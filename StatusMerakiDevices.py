import time
import meraki
from concurrent.futures import ThreadPoolExecutor
import config
import telegram
import datetime
import BaseDeDatos.Conexion_BD as Bd


bot_token = config.bot_token_telegram
chat_id = config.chat_id_telegram
bot = telegram.Bot(token=bot_token)

dashboard_name = config.dashboard_meraki
#executor = ThreadPoolExecutor(max_workers=3)
organization_id= config.id_org 
datos_db = config.var_empty
contador = 0
USER_MERAKI = config.var_empty
network_id = config.var_empty
dashboard= config.var_empty
network_name  = config.var_empty
url_network= config.var_empty
error = config.var_empty
conn = config.var_empty

def Process_Estado_Device():
    try:
        response_ex = dashboard.organizations.getOrganizationDevicesStatuses(
            organization_id, total_pages='all'
        )
            
        for dev2 in range(len(response_ex)):
            Ingresar_EStado_Dispositivos(response_ex,dev2)
            

    except Exception as ex: 
        bot.send_message(chat_id,text="Error en el Script Estado Dispositivos\n"+str(ex))
        error.write("Error al Procesar la peticion "+str(ex)+"\n")

def Ingresar_EStado_Dispositivos(response_ex,dev2):
    serie = str(response_ex[dev2]["serial"])
    cantidad = datos_db.Verificar_Dispositivo(serie)
    cantidad_inventario = datos_db.Process_Get_Devices_Count(serie)
    if cantidad == 0 and cantidad_inventario == 1:
        estado = (serie,str(response_ex[dev2]["status"]),"MERAKI")
        datos_db.Insertar_Estado_Dispositivos(estado)
    else:
        datos_db.Actualizar_Estado_Dispositivos(serie,str(response_ex[dev2]["status"]))

if __name__ == '__main__':
    error = open(config.merakiStatus_log,"w")
    datos_db = Bd.ConexionBaseDeDatos()
    USER_MERAKI = datos_db.Get_Dashboard_token(dashboard_name)
    dashboard = meraki.DashboardAPI(
                    USER_MERAKI,
                    output_log=False,
	                print_console=False
                )      
    error = open(config.merakiDevices_log,"w")
    while True:
        try:
            x = datetime.datetime.now()
            bot.send_message(chat_id,text="Script MERAKI Estado Dispositivos Iniciado....\n"+str(x.strftime("%c")))
            print("Script Meraki Estado Devices..."+str(x))
            Process_Estado_Device()
        except Exception as ex:
            #bot.send_message(chat_id,text="Error en el Script MERAKI Estado Dispositivos Iniciado\n"+str(x.strftime("%c")+"\n"+str(ex)))
            error.write("Error al Principal Estado: "+str(ex)+"\n")
            dashboard = meraki.DashboardAPI(
                    USER_MERAKI,
                    output_log=False,
	                print_console=False
                )
            

        


    


