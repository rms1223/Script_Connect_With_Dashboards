import time
import meraki
from concurrent.futures import ThreadPoolExecutor
import config
import telegram
import datetime
import BaseDeDatos.Conexion_BD as Bd

bot = telegram.Bot(token=config.TELEGRAM_BOT_TOKEN)

#executor = ThreadPoolExecutor(max_workers=3)
connection_mysqldb = config.EMPTY_NAME
USER_MERAKI = config.EMPTY_NAME
network_id = config.EMPTY_NAME
connection_meraki= config.EMPTY_NAME
error_meraki_script = config.EMPTY_NAME
conn = config.EMPTY_NAME

def process_status_device():
    try:
        response_ex = connection_meraki.organizations.getOrganizationDevicesStatuses(
            config.IDS_ORGANIZATION_MERAKI, total_pages='all'
        )
        for dev2 in range(len(response_ex)):
            save_status_device(response_ex,dev2)
            #executor.submit(Ingresar_EStado_Dispositivos,response_ex,dev2)

    except Exception as ex: 
        #bot.send_message(config.TELEGRAM_CHAT_ID,text="Error en el Script Estado Dispositivos\n"+str(ex))
        error_meraki_script.write("Error to connect with MERAKI: "+str(ex)+"\n")

def save_status_device(response_ex,dev2):
    device_serial = str(response_ex[dev2]["serial"])
    total_device_in_database = connection_mysqldb.verify_device_from_serial(device_serial)
    cantidad_inventario = connection_mysqldb.get_total_devices(device_serial)
    if total_device_in_database == 0 and cantidad_inventario == 1:
        status = (device_serial,str(response_ex[dev2]["status"]),"MERAKI")
        connection_mysqldb.insert_status_devices(status)
    else:
        connection_mysqldb.update_status_devices(device_serial,str(response_ex[dev2]["status"]))

def get_connection_meraki_dashboard():
    try:
        meraki_connection = meraki.DashboardAPI(
                    USER_MERAKI,
                    output_log=False,
	                print_console=False
                )
        return meraki_connection
    except Exception as ex:
        error_meraki_script.write("Error to connect with MERAKI: "+str(ex)+"\n")


if __name__ == '__main__':
    error_meraki_script = open(config.PATH_LOG_ERROR_STATUS_MERAKI,"w")
    connection_mysqldb = Bd.MysqlDb()
    USER_MERAKI = connection_mysqldb.get_dashboard_token_from_dashboard(config.NAME_DASHBOARD_MERAKI)
    connection_meraki = get_connection_meraki_dashboard()      
    error_meraki_script = open(config.PATH_LOG_ERROR_MERAKI,"w")
    while True:
        try:
            x = datetime.datetime.now()
            bot.send_message(config.TELEGRAM_CHAT_ID,text="Script MERAKI Estado Dispositivos Iniciado....\n"+str(x.strftime("%c")))
            print("Script Meraki Estado Devices..."+str(x))
            process_status_device()
        except Exception as ex:
            #bot.send_message(chat_id,text="Error en el Script MERAKI Estado Dispositivos Iniciado\n"+str(x.strftime("%c")+"\n"+str(ex)))
            error_meraki_script.write("Error to connect with MERAKI: "+str(ex)+"\n")
            connection_meraki = get_connection_meraki_dashboard()
            

        


    


