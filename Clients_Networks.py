import time
import meraki
from concurrent.futures import ThreadPoolExecutor, wait
from meraki.config import OUTPUT_LOG
import config
import telegram
import datetime
import BaseDeDatos.Conexion_BD as Bd
import Format_Data as FormatData
get_Format = FormatData.FormatterData()
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
ip_server = config.ips_server
temp_devices_data = []
id_network_codigo = {}
url_network_dic = {}

#------------------------------------------Pool de Threads-----------------------------------------------#
#executor = ThreadPoolExecutor(max_workers=2)
import mongoScript as mongodb
con_mongo = mongodb.Mongo_Database()

#------------------------Metodo para agregar Dispositivos Externos a la Red (Servidores, Impresoras)----------------------#
def Process_Clients_Devices():
    with ThreadPoolExecutor(max_workers=config.workers) as executor:
        try:
            con_mongo.Get_Connection_network_clients().delete_many({})
            for network in con_mongo.Get_Connection_Network().find({}):
                response = dashboard.networks.getNetworkClients(
                    network["idRed"], total_pages='all'
                )
                if response:
                    for lp in response:
                        executor.submit(Guardar_Dispositivos_Clientes,lp,network["codigo"],network["url"])
        except Exception as ex:
            error.write("Error process dispositivos cliente: "+str(ex)+"\n") 

def Guardar_Dispositivos_Clientes(lp,codigo_equipo,url):  
    if str(lp['ip']) in IpsReservadas:
        serie  = str(lp['ip']+"-"+codigo_equipo)
        valor = con_mongo.Get_Client_Id_Network(serie)
        if valor == 0:
            if str(lp['ip']) in ip_server:
                datos_dispositivos = get_Format.Get_Format_Client_Server(lp,codigo_equipo,url)

                con_mongo.Get_Connection_network_clients().insert_one(datos_dispositivos)
            elif str(lp['ip']) == "10.10.10.1" :
                if not str(lp['ip']).includes("Aruba"):      
                    datos_dispositivos = get_Format.Get_Format_Client_Router(lp,codigo_equipo,url)
                    con_mongo.Get_Connection_network_clients().insert_one(datos_dispositivos)
            else :
                datos_dispositivos = get_Format.Get_Format_Client_Print(lp,codigo_equipo,url)
                con_mongo.Get_Connection_network_clients().insert_one(datos_dispositivos)
        else:
            filtro  = {"serial":serie}
            valores = {"$set": { 'estado': str(lp['status']) } }
            con_mongo.Get_Connection_network_clients().update_one(filtro,valores)
            
#---------------------------------------------------------------------------Inicio de  Ejecucion del Script------------------------------------------------------------------------------#
if __name__ == '__main__':
    datos_db = Bd.ConexionBaseDeDatos()

    USER_MERAKI = datos_db.Get_Dashboard_token(dashboard_name)

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
            bot.send_message(chat_id,text="Script Meraki Dispositivos Iniciado....\n"+str(x.strftime("%c")))
            print("Script Clientes Meraki Iniciado..."+str(x))
            Process_Clients_Devices()
            time.sleep(config.espera)
        except Exception as ex:
            bot.send_message(chat_id,text="Error Script Meraki Dispositivos Iniciado....\n"+str(x.strftime("%c")+"\n"+str(ex)))
            dashboard = meraki.DashboardAPI(
                    USER_MERAKI,
                    output_log=False,
	                print_console=False
                )
        
