import time
import meraki
from concurrent.futures import ThreadPoolExecutor, wait

from meraki.config import OUTPUT_LOG
import config
import telegram
import datetime
import BaseDeDatos.Conexion_BD as Bd

#------------------------------------------Base de Datos------------------------------------------------------------#
datos_db=config.var_empty
#------------------------------------------Configuracion Bot Telegram-----------------------------------------------#
bot_token = config.bot_token_telegram
chat_id = config.chat_id_telegram
bot = telegram.Bot(token=bot_token)
#------------------------------------------Variables del Sistema----------------------------------------------------#
dashboard_name = config.dashboard_meraki
organization_id = config.id_org
IpsReservadas = config.ips_reservadas
IpsServer = config.ips_server
Carteles = config.carteles_sistema
contador = 0
USER_MERAKI = config.var_empty
network_id = config.var_empty
error = config.var_empty
conn = config.var_empty
codigo= config.var_empty
dashboard = config.var_empty
network_name  = config.var_empty
url_network= config.var_empty
temp_devices_data = []
id_network_codigo = {}
url_network_dic = {}

#------------------------------------------Pool de Threads-----------------------------------------------#
#executor = ThreadPoolExecutor(max_workers=2)
import mongoScript as mongodb
con_mongo = mongodb.Mongo_Database()
import DashboardAruba as Aruba
dash_aruba = Aruba.Equipos_Aruba_Dasboard()



def Process_Network():
    with ThreadPoolExecutor(max_workers=config.workers) as executor:
        try:
            response_networks = dashboard.organizations.getOrganizationNetworks(
                organization_id, total_pages='all',
            )
            for network in response_networks:
                executor.submit(Ingresar_Redes,network)    
        except Exception as ex:
            print("Exception "+str(ex)+"\n")
    datos_db.Actualizar_Estado_Proceso("ACTUALIZANDO")
    con_mongo.Get_Connection_Devices().delete_many({})
    con_mongo.Get_Connection().delete_many({})
    Process_Get_Devices()
    Process_Estado_Device()
    Process_Template()
    request_aruba = dash_aruba.Procesar_Peticion_Aruba()
    request_aruba_switch = dash_aruba.Procesar_Peticion_Aruba_Switches()
    if not request_aruba:
        dash_aruba.Procesar_Peticion_Aruba()
    if not request_aruba_switch:
        dash_aruba.Procesar_Peticion_Aruba_Switches()
    request_aruba = dash_aruba.Procesar_Peticion_Aruba_AP()
    datos_db.Actualizar_Estado_Proceso("LISTO")  

    x = datetime.datetime.now()
    print("Proceso Finalizado..."+str(x)) 

def verify_template(network):
    return network["configTemplateId"] if "configTemplateId" in network else "No especificado"

#------------------------------Agrega Las redes creadas en el dashboard de Meraki en la Base de datos--------------#
def Ingresar_Redes(network):
    network_id = network["id"]
    network_name = network["name"]
    url_network = network["url"]
    val = network["tags"]
    
    if len(val) != 0 :
        if str(val[0]) in Carteles:
            codigo = str(val[1])
        else:
            codigo = str(val[0])
    datos_redes = {"idRed":str(network_id),"nombre":str(network_name),"tags":str(val),"url":str(url_network),"codigo":codigo,"id_template":verify_template(network)}
    '''Metodos para guadarlos en MOngo'''
    con_mongo.Get_Connection_Network().insert_one(datos_redes)
    '''Fin de Metodos'''
    id_network_codigo[network_id] = codigo
    url_network_dic[network_id] = url_network


def Process_Estado_Device():
    with ThreadPoolExecutor(max_workers=config.workers) as executor:
        try:
            response_ex = dashboard.organizations.getOrganizationDevicesStatuses(
                organization_id, total_pages='all'
            )
            for dev2 in range(len(response_ex)):
                executor.submit(Ingresar_EStado_Dispositivos,response_ex,dev2)
        except Exception as ex: 
            bot.send_message(chat_id,text="Error en el Script Estado Dispositivos\n"+str(ex))
            error.write("Error al Procesar la peticion "+str(ex)+"\n")

def Ingresar_EStado_Dispositivos(response_ex,dev2):
    serie = str(response_ex[dev2]["serial"])
    estado = {"serial_equipo":serie,"estado":str(response_ex[dev2]["status"]),"dashboard":"MERAKI"}
    con_mongo.Get_Connection().insert_one(estado)



#------------------------------Agrega dispositivos de Red a la Base de datos-----------------------------------------#
def Process_Get_Devices():
    try:  
        response_data = dashboard.organizations.getOrganizationDevices(
            organization_id, total_pages='all'
        )
        
        con_mongo.Get_Connection_Devices().insert_many(response_data)
    except Exception as ex:
        error.write("No existen registros "+str(ex)+"\n")
    

#------------------------------Agrega los Templates de las redes a la base de datos----------------------------------#    

def Process_Template():
    try:
        response_template = dashboard.organizations.getOrganizationConfigTemplates(
            organization_id
        )
        con_mongo.Get_Connection_template().delete_many({})
        con_mongo.Get_Connection_template().insert_many(response_template)
    except Exception as ex:
         error.write("Error en Process Template "+str(ex)+"\n")

def verify_tags(doc):
    return doc['tags'] if "tags" in doc else "NO TAGS"
#---------------------------------------------------------------------------Inicio de  Ejecucion del Script------------------------------------------------------------------------------#
if __name__ == '__main__':
    datos_db = Bd.ConexionBaseDeDatos()
    USER_MERAKI = datos_db.Get_Dashboard_token(dashboard_name)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#------------------------Inicializacion de variables para la conexion con el dashboard Meraki----------------------#
    dashboard = meraki.DashboardAPI(
                    USER_MERAKI,
                    output_log=False,
	                print_console=False
                )
    
    error = open(config.merakiDevices_log,"w")
    while True:
        try:
            
            x = datetime.datetime.now()
            print("Script Meraki Iniciado..."+str(x))
            con_mongo.Get_Connection_Network().delete_many({})
            con_mongo.Get_Connection_Devices().delete_many({})
            Process_Network()
            time.sleep(config.espera)
        except Exception as ex:
            dashboard = meraki.DashboardAPI(
                    USER_MERAKI,
                    output_log=False,
	                print_console=False
                )
        
