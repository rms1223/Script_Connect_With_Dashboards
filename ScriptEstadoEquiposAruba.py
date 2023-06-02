import time
from concurrent.futures import ThreadPoolExecutor
import config
import ArchivosAruba.var_aruba as var_aruba
import requests as request
import datetime
import telegram
import BaseDeDatos.Conexion_BD as Bd

##Botde Telegram 
bot_token = config.TELEGRAM_BOT_TOKEN
chat_id = config.TELEGRAM_CHAT_ID
bot = telegram.Bot(token=bot_token)

#------------------------Datos Configuracion Token Aruba#-------------------------------------
USER_ARUBA = config.EMPTY_NAME
USER_REFRESH_TOKEN_ARUBA = config.EMPTY_NAME
base_url= config.ARUBA_BASE_URL
search_url = config.ARUBA_URL_SEARCH_GATEWAYS

contador = 0
dashboard= config.NAME_DASHBOARD_ARUBA
executor = ThreadPoolExecutor(max_workers=2)
error = config.EMPTY_NAME
conn = config.EMPTY_NAME
cantidad =0
datos_db = config.EMPTY_NAME

def Nuevo_Token():
    try:
        global USER_REFRESH_TOKEN_ARUBA
        global USER_ARUBA
        get_R_url = base_url+config.ARUBA_URL_REFRESH_TOKEN

        data = {
            var_aruba.id : config.ID_CLIENTE_ARUBA,
            var_aruba.secret : config.SECRET_CLIENT_ARUBA,
            var_aruba.type: config.TYPE_ARUBA_TOKEN,
            var_aruba.refresh_token: USER_REFRESH_TOKEN_ARUBA
        }
        x = datetime.datetime.now()
        app_call = request.post(get_R_url,params=data)
        val =  app_call.json()
        USER_ARUBA = str(val[var_aruba.access_token])
        USER_REFRESH_TOKEN_ARUBA = str(val[var_aruba.refresh_token])
        datos_db.update_dashboard_token(USER_ARUBA,USER_REFRESH_TOKEN_ARUBA,dashboard)
        bot.send_message(chat_id,text="Nuevo Token Aruba Generado....\n"+str(x.strftime("%c")))
    except Exception as ex:
        error.write("Error al Regenerar el token "+str(ex))
    
def Procesar_Peticion_Aruba():
    try:
        get_R_url = base_url+search_url
        header = {"Authorization":f"bearer "+USER_ARUBA}
        app_call = request.get(get_R_url,headers=header)
        val =  app_call.json()
        if "message" not in val:
            for i in val["gateways"]:
                if i["site"] == None:
                    datos = (str(i["serial"]), str(i["name"]),"10.10.10.1 ",str(i["macaddr"]),str(i["model"]),str(i["labels"]),"")
                    redes_cartel = (str(i["name"])+"|"+str(i["serial"]),str(i["group_name"]),str(i["labels"])+" "+str(i["group_name"]),"")
                else:
                    datos = (str(i["serial"]), str(i["name"]),"10.10.10.1 ",str(i["macaddr"]),str(i["model"]),str(i["labels"])+" "+str(i["group_name"]),"")
                    redes_cartel = (str(i["group_name"])+"|"+str(i["serial"]),str(i["site"]),str(i["labels"])+" "+str(i["group_name"]),"")
                estado = (str(i["serial"]),str(i["status"]),"ARUBA")
                cantidad = datos_db.get_total_devices(str(i["serial"]))
                if  cantidad == 0 :
                    datos_db.insert_networkdevices_in_mysql(datos)
                    datos_db.insert_status_devices(estado)
                    datos_db.insert_network_in_mysql(redes_cartel)
                else:
                    datos_db.update_status_devices(str(i["serial"]),str(i["status"]))      
    except:
        Nuevo_Token()


if __name__ == '__main__':
    error = open(config.PATH_FILE_ERROR_ARUBA,"w")
    datos_db = Bd.MysqlDb()
    USER_REFRESH_TOKEN_ARUBA = datos_db.get_dashboard_refreshtoken_from_dashboard(dashboard)
    USER_ARUBA = datos_db.get_dashboard_token_from_dashboard(dashboard)
    x = datetime.datetime.now()
    bot.send_message(chat_id,text="Script Aruba Dispositivos Iniciado....\n"+str(x.strftime("%c")))
    while True:
        try:
            x = datetime.datetime.now()
            print("Inicio de Ejecucion......."+str(x))
            Procesar_Peticion_Aruba()
            time.sleep(300)
        except Exception as ex:
            bot.send_message(chat_id,text="Error en el Script Aruba Dispositivos....\n"+str(x.strftime("%c")))
        


