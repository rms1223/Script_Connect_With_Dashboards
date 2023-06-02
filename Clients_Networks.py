import time
import meraki
from concurrent.futures import ThreadPoolExecutor, wait

from meraki.config import OUTPUT_LOG
import config
import telegram
import datetime
import BaseDeDatos.Conexion_BD as Bd

#------------------------------------------Base de Datos------------------------------------------------------------#
datos_db=config.EMPTY_NAME
#------------------------------------------Configuracion Bot Telegram-----------------------------------------------#
bot_token = config.TELEGRAM_BOT_TOKEN
chat_id = config.TELEGRAM_CHAT_ID
bot = telegram.Bot(token=bot_token)
#------------------------------------------Variables del Sistema----------------------------------------------------#
dashboard_name = config.NAME_DASHBOARD_MERAKI
organization_id = config.IDS_ORGANIZATION_MERAKI
IpsReservadas = config.IPS_RESERVED
Carteles = config.CARTELES_LICITACIONES
contador = 0
USER_MERAKI = config.EMPTY_NAME
network_id = config.EMPTY_NAME
error = config.EMPTY_NAME
conn = config.EMPTY_NAME
codigo= config.EMPTY_NAME
dashboard = config.EMPTY_NAME
network_name  = config.EMPTY_NAME
url_network= config.EMPTY_NAME
ip_server = ["10.10.10.3","10.10.10.4","10.10.10.5"]
temp_devices_data = []
id_network_codigo = {}
url_network_dic = {}

#------------------------------------------Pool de Threads-----------------------------------------------#
#executor = ThreadPoolExecutor(max_workers=2)
import mongoScript as mongodb
con_mongo = mongodb.Mongo_Database()

####Metodo para agregar Clientes como servidores y ROUTER que no son meraki 
def process_meraki_clients_networks():
    with ThreadPoolExecutor(max_workers=config.PROCESS_WORKER) as executor:
        try:
            con_mongo.get_mongodb_network_clients().delete_many({})
            for network in con_mongo.get_mongodb_network().find({}):
                response = dashboard.networks.getNetworkClients(
                    network["idRed"], total_pages='all'
                )
                if response:
                    for lp in response:
                        executor.submit(save_clients_devices,lp,network["codigo"],network["url"])
        except Exception as ex:
            error.write("Error process dispositivos cliente: "+str(ex)+"\n") 

def save_clients_devices(lp,codigo_equipo,url):  
    if str(lp['ip']) in IpsReservadas:
        serie  = str(lp['ip']+"-"+codigo_equipo)
        valor = con_mongo.get_mongodb_clients_from_idnetwork(serie)
        if valor == 0:
            if str(lp['ip']) in ip_server:
                datos_dispositivos = {"serial":str(lp['ip']+"-"+codigo_equipo),"nombre":str(lp['description']+" "+codigo_equipo),"ip":str(lp['ip']),"mac":str(lp['mac']),"modelo":str(lp['manufacturer']),"tags":"SERVER "+codigo_equipo,"estado":str(lp['status']),"codigo":codigo_equipo,"ruta":url} 
                con_mongo.get_mongodb_network_clients().insert_one(datos_dispositivos)
            elif str(lp['ip']) == "10.10.10.1" :
                if not str(lp['ip']).includes("Aruba"):      
                    datos_dispositivos = {"serial":str(lp['ip']+"-"+codigo_equipo),"nombre":str(lp['manufacturer']+" "+codigo_equipo),"ip":str(lp['ip']),"mac":str(lp['mac']),"modelo":str(lp['manufacturer']),"tags":"ROUTER "+codigo_equipo,"estado":str(lp['status']),"codigo":codigo_equipo,"ruta":url}
                    con_mongo.get_mongodb_network_clients().insert_one(datos_dispositivos)
            else :
                datos_dispositivos = {"serial":str(lp['ip']+"-"+codigo_equipo),"nombre":str(lp['manufacturer']+" "+codigo_equipo),"ip":str(lp['ip']),"mac":str(lp['mac']),"modelo":str(lp['manufacturer']),"tags":"IMPRESORAS "+codigo_equipo,"estado":str(lp['status']),"codigo":codigo_equipo,"ruta":url}
                con_mongo.get_mongodb_network_clients().insert_one(datos_dispositivos)
        else:
            filtro  = {"serial":serie}
            valores = {"$set": { 'estado': str(lp['status']) } }
            con_mongo.get_mongodb_network_clients().update_one(filtro,valores)
##-------------------------------------------------------------------------###
if __name__ == '__main__':
    datos_db = Bd.MysqlDb()
    ##Cargamos lostoken de los Dashboard
    USER_MERAKI = datos_db.get_dashboard_token_from_dashboard(dashboard_name)

    ##Inicializamos la variables para manejar laspeticiones dashboard meraki
    dashboard = meraki.DashboardAPI(
                    USER_MERAKI,
                    output_log=False,
	                print_console=False
                )
    
    error = open(config.PATH_FILE_ERROR_MERAKI,"w")
    while True:
        try:
            x = datetime.datetime.now()
            bot.send_message(chat_id,text="Script Meraki Dispositivos Iniciado....\n"+str(x.strftime("%c")))
            print("Script Clientes Meraki Iniciado..."+str(x))
            process_meraki_clients_networks()
            time.sleep(config.PROCESS_WAIT)
        except Exception as ex:
            bot.send_message(chat_id,text="Error Script Meraki Dispositivos Iniciado....\n"+str(x.strftime("%c")+"\n"+str(ex)))
            dashboard = meraki.DashboardAPI(
                    USER_MERAKI,
                    output_log=False,
	                print_console=False
                )
        
