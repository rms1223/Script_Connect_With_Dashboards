import time
import meraki
from concurrent.futures import ThreadPoolExecutor, wait

from meraki.config import OUTPUT_LOG
import config
import telegram
import datetime
import BaseDeDatos.Conexion_BD as Bd

#------------------------------------------Base de Datos------------------------------------------------------------#
#__connection_mysql=config.EMPTY_NAME
#------------------------------------------Configuracion Bot Telegram-----------------------------------------------#
bot_token = config.TELEGRAM_BOT_TOKEN
chat_id = config.TELEGRAM_CHAT_ID
bot = telegram.Bot(token=bot_token)
error_mongo_db = open(config.PATH_FILE_ERROR_MONGODB,"w")
error_meraki_script = open(config.PATH_FILE_ERROR_MERAKI,"w")
#------------------------------------------Variables del Sistema----------------------------------------------------#
contador = 0
USER_MERAKI = config.EMPTY_NAME
network_id = config.EMPTY_NAME
error_meraki_dashboard = config.EMPTY_NAME
conn = config.EMPTY_NAME
codigo= config.EMPTY_NAME
meraki_dashboard_connection = config.EMPTY_NAME
network_name  = config.EMPTY_NAME
url_network= config.EMPTY_NAME
__id_network_codigo = {}
__url_network_dic = {}
__total_devices_in_meraki = 0

#executor = ThreadPoolExecutor(max_workers=2)
import mongoScript as mongodb
CONNECTION_MONGODB = mongodb.Mongo_Database()
import DashboardAruba as Aruba
ARUBA_DASHBOARD = Aruba.ArubaDevices()
import sdwancisco as Viptela
CISCO_VIPTELA_DASHBOARD = Viptela.ViptelaDevices()
import Huawei_Dashboard as Huawei
HUAWEI_DASHBOARD = Huawei.HuaweiDevices()

def process_huawei_dashboard():
    HUAWEI_DASHBOARD.read_huawei_devices_from_file()

def init_process_viptela_cisco():
    __connection_mysql.update_status_query_process("LISTO")
    CISCO_VIPTELA_DASHBOARD.start_process()

def process_aruba():
    __connection_mysql.update_status_query_process("LISTO")
    ARUBA_DASHBOARD.process_query_aruba_gateways()
    ARUBA_DASHBOARD.process_query_aruba_switch()
    ARUBA_DASHBOARD.process_query_aruba_ap()

def process_networks_meraki(org_id):
    with ThreadPoolExecutor(max_workers=config.PROCESS_WORKER) as executor:
        try:
            response_networks = meraki_dashboard_connection.organizations.getOrganizationNetworks(
                org_id, total_pages='all',
            )
            for network in response_networks:
                executor.submit(save_networks_from_meraki,network)    
        except Exception as meraki_script_error:
            error_meraki_script.write("Error Process Query MongoDB "+str(meraki_script_error)+"\n")
    
    process_devices_meraki_from_organizationid(org_id)
    process_status_devices_meraki_from_organizationid(org_id)
    process_templates_meraki_from_organizationid(org_id)
    __connection_mysql.update_status_query_process("LISTO")

def verify_meraki_template(network):
    return network["configTemplateId"] if "configTemplateId" in network else "No especificado"

def save_networks_from_meraki(reponse_meraki_network):
    try:
        id_network_meraki = reponse_meraki_network["id"]
        network_name_meraki = reponse_meraki_network["name"]
        url_network_meraki = reponse_meraki_network["url"]
        response_query_meraki = reponse_meraki_network["tags"]
        
        if len(response_query_meraki) != 0 :
            if str(response_query_meraki[0]) in config.CARTELES_LICITACIONES:
                codigo = str(response_query_meraki[1])
            else:
                codigo = str(response_query_meraki[0])
        datos_redes = {"idRed":str(id_network_meraki),
                       "nombre":str(network_name_meraki),
                       "tags":str(response_query_meraki),
                       "url":str(url_network_meraki),
                       "codigo":codigo,
                       "id_template":verify_meraki_template(reponse_meraki_network)
                    }
        
        CONNECTION_MONGODB.get_mongodb_network().insert_one(datos_redes)
        __id_network_codigo[id_network_meraki] = codigo
        __url_network_dic[id_network_meraki] = url_network_meraki
    except Exception as mongodb_error:
        error_mongo_db.write("Error Process Query MongoDB "+str(mongodb_error)+" - "+codigo+"\n")

def process_status_devices_meraki_from_organizationid(meraki_organization_id):
    with ThreadPoolExecutor(max_workers=config.PROCESS_WORKER) as executor:
        try:
            response_ex = meraki_dashboard_connection.organizations.getOrganizationDevicesStatuses(
                meraki_organization_id, total_pages='all'
            )
            CONNECTION_MONGODB.get_mongodb_status_device_temporal().insert_many(response_ex)
        except Exception as mongodb_error:
            error_mongo_db.write("Error Process Query MongoDB "+str(mongodb_error)+"\n")

def process_devices_meraki_from_organizationid(meraki_organization_id):
    global __total_devices_in_meraki
    try:  
        response_data = meraki_dashboard_connection.organizations.getOrganizationDevices(
            meraki_organization_id, total_pages='all'
        )
        __total_devices_in_meraki += len(response_data)
        CONNECTION_MONGODB.get_mongodb_devices_temporal().insert_many(response_data)
    except Exception as mongodb_error:
        error_mongo_db.write("Error Process Query MongoDB "+str(mongodb_error)+"\n")
     
def process_templates_meraki_from_organizationid(meraki_organization_id):
    try:
        response_meraki_template = meraki_dashboard_connection.organizations.getOrganizationConfigTemplates(
            meraki_organization_id
        )
        CONNECTION_MONGODB.get_mongodb_template().insert_many(response_meraki_template)
    except Exception as mongodb_error:
        error_mongo_db.write("Error Process Query MongoDB "+str(mongodb_error)+"\n")

def verify_tags(tags):
    return tags['tags'] if "tags" in tags else "NO TAGS"

def save_register_in_mongodatabase():
    try:
        CONNECTION_MONGODB.get_mongodb_devices().delete_many({})
        CONNECTION_MONGODB.get_mongodb_devices_temporal().aggregate([{"$out":"devices"}])
        time.sleep(3)
        CONNECTION_MONGODB.get_mongodb_devices_status().delete_many({})
        CONNECTION_MONGODB.get_mongodb_status_device_temporal().aggregate([{"$out":"devices_status"}])
    except Exception as mongodb_error:
        error_mongo_db.write("Error Process Query MongoDB "+str(mongodb_error)+"\n")
    

def delete_register_from_mongodb():
    try:
        CONNECTION_MONGODB.get_mongodb_network().delete_many({})
        CONNECTION_MONGODB.get_mongodb_devices_temporal().delete_many({})
        CONNECTION_MONGODB.get_mongodb_status_device_temporal().delete_many({})
        CONNECTION_MONGODB.get_mongodb_template().delete_many({})
    except Exception as mongodb_error:
        error_mongo_db.write("Error Process Query MongoDB "+str(mongodb_error)+"\n")
    

def get_connection_meraki_dashboard():
    try:
        meraki_connection = meraki.DashboardAPI(
                    USER_MERAKI,
                    output_log=False,
	                print_console=False
                )
        return meraki_connection
    except Exception as ex:
        print(f"Error to conect with MERAKI DASHBOARD {ex}")

if __name__ == '__main__':
    __connection_mysql = Bd.MysqlDb()
    USER_MERAKI = __connection_mysql.get_dashboard_token_from_dashboard(config.NAME_DASHBOARD_MERAKI)
    meraki_dashboard_connection = get_connection_meraki_dashboard()
    error_meraki_dashboard = open(config.PATH_FILE_ERROR_MERAKI,"w")
    while True:
        try:
            __total_devices_in_meraki =0
            time_query = datetime.datetime.now()
            print(f"Scripts Iniciado... {str(time_query)}")
            delete_register_from_mongodb()
            print("MERAKI")
            for id_organization in config.IDS_ORGANIZATION_MERAKI:
                process_networks_meraki(id_organization)
            
            print("Total de datos en BD "+str(__connection_mysql.verify_total_devices_in_dashboards("Meraki",__total_devices_in_meraki)))
            print(f"Total Meraki {str(__total_devices_in_meraki)}")
            print("HUAWEI")
            process_huawei_dashboard()
            print("ARUBA")
            process_aruba()
            print("VIPTELA")
            init_process_viptela_cisco()
            save_register_in_mongodatabase()
            time_query = datetime.datetime.now()
            print(f"Scripts Finalizado... {str(time_query)}")
            time.sleep(config.PROCESS_WAIT)
        except Exception as meraki_script_error:
            error_meraki_script.write("Error Process Query MongoDB "+str(meraki_script_error)+"\n")
            meraki_dashboard_connection = get_connection_meraki_dashboard()
            time.sleep(config.PROCESS_WAIT)
        
