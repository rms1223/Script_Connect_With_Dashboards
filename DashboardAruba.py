import time
from concurrent.futures import ThreadPoolExecutor
import config
import ArchivosAruba.var_aruba as var_aruba
import requests as request
import datetime
import telegram
import BaseDeDatos.Conexion_BD as Bd
import mongoScript as mongodb
import Format_Data as FormatData

class Equipos_Aruba_Dasboard:
#----------------------------------------------Datos Bot Telegram---------------------------------------------------------#
    bot_token = config.bot_token_telegram
    chat_id = config.chat_id_telegram
    bot = telegram.Bot(token=bot_token)

#----------------------------------------------Datos Configuracion Token Aruba---------------------------------------------#
    USER_ARUBA = config.var_empty
    USER_REFRESH_TOKEN_ARUBA = config.var_empty
    base_url= config.base_url_aruba
    search_url = config.url_buscar_dispositivos
    contador = 0
    dashboard= config.dashboard_aruba
    executor = ThreadPoolExecutor(max_workers=2)
    error = config.var_empty
    conn = config.var_empty
    cantidad =0
    datos_db = config.var_empty
    con_mongo = mongodb.Mongo_Database()
    get_Format = FormatData.FormatterData()

    def __init__(self):
        self.datos_db = Bd.ConexionBaseDeDatos()
        self.USER_REFRESH_TOKEN_ARUBA = self.datos_db.Get_Dashboard_RefreshToken(self.dashboard)
        self.USER_ARUBA = self.datos_db.Get_Dashboard_token(self.dashboard)

#------------------------------Metodo que Genera un nuevo token en el central de Aruba----------------------------------------#
    def Nuevo_Token(self):
        try:
            global USER_REFRESH_TOKEN_ARUBA
            global USER_ARUBA
            get_R_url = self.base_url+config.url_refreshToken

            data = {
                var_aruba.id : config.client_id,
                var_aruba.secret : config.client_secret,
                var_aruba.type: config.tipo,
                var_aruba.refresh_token: self.USER_REFRESH_TOKEN_ARUBA
            }
            x = datetime.datetime.now()
            app_call = request.post(get_R_url,params=data)
            val =  app_call.json()
            self.USER_ARUBA = str(val[var_aruba.access_token])
            self.USER_REFRESH_TOKEN_ARUBA = str(val[var_aruba.refresh_token])
            self.datos_db.Set_Dashboard_Tokens(self.USER_ARUBA,self.USER_REFRESH_TOKEN_ARUBA,self.dashboard)
            self.bot.send_message(self.chat_id,text="Nuevo Token Aruba Generado....\n"+str(x.strftime("%c")))
        except Exception as ex:
            self.error.write("Error al Regenerar el token "+str(ex))

#------------------------------Agrega dispositivos de Red (switch) a la Base de datos-----------------------------------------#
    def Procesar_Peticion_Aruba_Switches(self):
        try:
            get_R_url = self.base_url+config.url_buscar_switch
            header = {"Authorization":f"bearer "+self.USER_ARUBA}
            app_call = request.get(get_R_url,headers=header)
            val =  app_call.json()
            if "message" not in val:
                for i in val["switches"]:
                    datos = self.get_Format.Get_Format_Switch(i)
                    if i["site"] == None:
                        redes_cartel = self.get_Format.Get_Format_RedesCartel_Name(i)
                    else:
                        redes_cartel = self.get_Format.Get_Format_RedesCartel_GroupName(i)
                    estado = self.get_Format.Get_Format_Status(i)
                    cantidad = self.con_mongo.Get_Connection_Devices().count_documents({"serial": str(i["serial"])})
                    if  cantidad == 0 :
                        self.con_mongo.Get_Connection_Devices().insert_one(datos)
                    self.con_mongo.Get_Connection().insert_one(estado)
                    self.con_mongo.Get_Connection_Network().insert_one(redes_cartel)
            return True         
        except Exception as ex:
            print(str(ex))
            self.Nuevo_Token()
            return False
#------------------------------Agrega dispositivos de Red (APs) a la Base de datos-------------------------------------------#
    def Procesar_Peticion_Aruba_AP(self):
        try:
            get_R_url = self.base_url+config.url_buscar_aps
            header = {"Authorization":f"bearer "+self.USER_ARUBA}
            app_call = request.get(get_R_url,headers=header)
            val =  app_call.json()
            if "message" not in val:
                for i in val["aps"]:
                    datos = self.get_Format.Get_Format_Ap(i)
                    if i["site"] == None:
                        
                        redes_cartel = self.get_Format.Get_Format_RedesCartel_Name(i)
                    else:
                        redes_cartel = self.get_Format.Get_Format_RedesCartel_GroupName(i)
                    estado = self.get_Format.Get_Format_Status(i)
                    cantidad = self.con_mongo.Get_Connection_Devices().count_documents({"serial": str(i["serial"])})
                    if  cantidad == 0 :
                        self.con_mongo.Get_Connection_Devices().insert_one(datos)
                    self.con_mongo.Get_Connection().insert_one(estado)
                    self.con_mongo.Get_Connection_Network().insert_one(redes_cartel)
            return True         
        except Exception as ex:
            print(str(ex))
            self.Nuevo_Token()
            return False
#------------------------------Agrega dispositivos de Red (Router) a la Base de datos-----------------------------------------#
    def Procesar_Peticion_Aruba(self):
        try:
            get_R_url = self.base_url+self.search_url
            header = {"Authorization":f"bearer "+self.USER_ARUBA}
            app_call = request.get(get_R_url,headers=header)
            val =  app_call.json()
            if "message" not in val:
                for i in val["gateways"]:
                    datos = self.get_Format.Get_Format_Gateway(i)
                    if i["site"] == None:
                        redes_cartel = self.get_Format.Get_Format_RedesCartel_Name(i)
                    else:
                        redes_cartel = self.get_Format.Get_Format_RedesCartel_GroupName(i)
                    estado = self.get_Format.Get_Format_Status(i)
                    cantidad = self.con_mongo.Get_Connection_Devices().count_documents({"serial": str(i["serial"])})
                    if cantidad ==  0:
                        self.con_mongo.Get_Connection_Devices().insert_one(datos)
                    self.con_mongo.Get_Connection().insert_one(estado)
                    self.con_mongo.Get_Connection_Network().insert_one(redes_cartel)
            return True
        except Exception as ex:
            print(str(ex))
            self.Nuevo_Token()
            return False

        


