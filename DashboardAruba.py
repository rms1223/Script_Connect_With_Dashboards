import time
from concurrent.futures import ThreadPoolExecutor
import config
import ArchivosAruba.var_aruba as var_aruba
import requests as request
import datetime
import telegram
import BaseDeDatos.Conexion_BD as Bd
import mongoScript as mongodb
import Devices as dev
import math
import BaseDeDatos.Conexion_BD as Bd

class ArubaDevices:
    ##Botde Telegram 
    bot = telegram.Bot(token=config.TELEGRAM_BOT_TOKEN)

    #------------------------Datos Configuracion Token Aruba#-------------------------------------
    __USER_ARUBA = config.EMPTY_NAME
    __USER_REFRESH_TOKEN_ARUBA = config.EMPTY_NAME
    __error = config.EMPTY_NAME
    conn = config.EMPTY_NAME
    cantidad =0

    data_ap = []
    __status_device_array = []
    __offset = 0
    __total_devices_aruba = 0
    __conection_mysql_db = Bd.MysqlDb()
    __connection_mongodb = mongodb.Mongo_Database()

    def __init__(self):
        self.__conection_mysql_db = Bd.MysqlDb()
        self.__USER_REFRESH_TOKEN_ARUBA = self.__conection_mysql_db.get_dashboard_refreshtoken_from_dashboard(config.NAME_DASHBOARD_ARUBA)
        self.__USER_ARUBA = self.__conection_mysql_db.get_dashboard_token_from_dashboard(config.NAME_DASHBOARD_ARUBA)


    def generate_new_token_aruba_dashboard(self):
        try:
            global USER_REFRESH_TOKEN_ARUBA
            global USER_ARUBA
            PATH_BASE_ARUBA_DASHBOARD = config.ARUBA_BASE_URL+config.ARUBA_URL_REFRESH_TOKEN

            DATA_QUERY_ARUBA_DASHBOARD = {
                config.ARUBA_NAME_ID : config.ID_CLIENTE_ARUBA,
                config.ARUBA_NAME_SECRET : config.SECRET_CLIENT_ARUBA,
                config.ARUBA_NAME_TYPE: config.TYPE_ARUBA_TOKEN,
                config.ARUBA_NAME_REFRESH_TOKEN: self.__USER_REFRESH_TOKEN_ARUBA
            }
            time_query = datetime.datetime.now()
            SEND_QUERY = request.post(PATH_BASE_ARUBA_DASHBOARD,params=DATA_QUERY_ARUBA_DASHBOARD)
            response_query_to_json =  SEND_QUERY.json()
            self.__USER_ARUBA = str(response_query_to_json[var_aruba.access_token])
            self.__USER_REFRESH_TOKEN_ARUBA = str(response_query_to_json[var_aruba.refresh_token])
            self.__conection_mysql_db.update_dashboard_token(self.__USER_ARUBA,self.__USER_REFRESH_TOKEN_ARUBA,config.NAME_DASHBOARD_ARUBA,time_query.strftime("%c"))
            #self.bot.send_message(config.TELEGRAM_CHAT_ID,text="Nuevo Token Aruba Generado....\n"+str(x.strftime("%c")))
        except Exception as ex:
            print(str(ex))
            self.__error.write("Error al Regenerar el token "+str(ex))

    def process_query_aruba_switch(self):
        try:
            data_device_switch =[]
            estado_array = []
            PATH_ARUBA_SWITCH = config.ARUBA_BASE_URL+config.ARUBA_URL_SEARCH_SWITCH
            HEADER_QUERY_ARUBA = {"Authorization":f"bearer "+self.__USER_ARUBA}
            SEND_QUERY_ARUBA_SWITCH = request.get(PATH_ARUBA_SWITCH,headers=HEADER_QUERY_ARUBA)
            response_query_to_json =  SEND_QUERY_ARUBA_SWITCH.json()
            if "message" not in response_query_to_json:
                for i in response_query_to_json["switches"]:
                    data_device_aruba_switch = {
                            "serial":str(i["serial"]),
                            "name":str(i["name"]),
                            "lanIp":str(i["ip_address"]),
                            "mac":str(i["macaddr"]),
                            "model":str(i["model"]),
                            "notes":"",
                            "tags":["ARUBA SWITCH"],
                            "url":"ARUBA"
                        }
                    if i["site"] == None:
                        
                        redes_cartel = {
                                        "idRed":str(i["name"])+"|"+str(i["serial"]),
                                        "nombre":str(i["group_name"]),
                                        "tags":str(i["labels"])+" "+str(i["group_name"]),
                                        "url":"ARUBA"}
                    else:
                        redes_cartel = {
                                        "idRed":str(i["group_name"])+"|"+str(i["serial"]),
                                        "nombre":str(i["site"]),
                                        "tags":str(i["labels"])+" "+str(i["group_name"]),
                                        "url":"ARUBA"}
                    estado = {
                                "serial":str(i["serial"]),
                                "status":str(i["status"]),
                                "dashboard":"ARUBA"}
                    total_devices_in_database_from_serial = self.__connection_mongodb.get_mongodb_devices_temporal().count_documents({"serial": str(i["serial"])})
                    if  total_devices_in_database_from_serial == 0 :
                        data_device_switch.append(data_device_aruba_switch)
                    estado_array.append(estado)
                    self.__connection_mongodb.get_mongodb_network().insert_one(redes_cartel)
            self.__total_devices_aruba += len(data_device_switch)
            self.__connection_mongodb.get_mongodb_devices_temporal().insert_many(data_device_switch)
            time.sleep(5)
            self.__connection_mongodb.get_mongodb_status_device_temporal().insert_many(estado_array)
                    
            return True         
        except Exception as ex:
            print(str(ex))
            self.generate_new_token_aruba_dashboard()
            return False


    def generate_query_aps_to_json(self, isFirst,offset):
        if isFirst:
            SEND_QUERY_ARUBA_APS = config.ARUBA_BASE_URL+config.ARUBA_URL_SEARCH_APS
        else:
            SEND_QUERY_ARUBA_APS = config.ARUBA_BASE_URL+f"monitoring/v2/aps?offset={offset}&limit=1000"
        header = {"Authorization":f"bearer "+self.__USER_ARUBA}
        app_call = request.get(SEND_QUERY_ARUBA_APS,headers=header)
        return app_call.json()

    def process_query_aruba_ap(self):
        try:
            self.data_ap.clear()
            self.__status_device_array.clear()
            val =  self.generate_query_aps_to_json(True,0)

            total_devices_aps_from_query_aruba = val['total']

            self.__offset = (math.ceil(total_devices_aps_from_query_aruba / 1000)*1000)

            if "message" not in val:
                for data_in_response in val["aps"]:
                    devices = dev.Devices(str(data_in_response["serial"]).strip(),str(data_in_response["name"]).strip(),
                                          str(data_in_response["ip_address"]),str(data_in_response["macaddr"]),
                                          str(data_in_response["model"]),str(data_in_response["notes"]),
                                          "AP","ARUBA","ARUBA")
                    datos = {
                            "serial":str(devices.get_serial_device()[0]),
                            "name":str(devices.get_name_device()[0]),
                            "lanIp":str(devices.get_lanip_device()[0]),
                            "mac":str(devices.get_macaddress_device()[0]),
                            "model":str(devices.get_model_device()[0]),
                            "notes":str(devices.get_notes_device()[0]),
                            "tags":[str(devices.get_path_device()[0]), "AP"],
                            "url": str(devices.get_path_device()[0])
                        }
                    if data_in_response["site"] == None:
                        redes_cartel = {
                                        "idRed":str(devices.get_name_device()[0])+"|"+str(devices.get_serial_device()[0]),
                                        "nombre":str(data_in_response["group_name"]),
                                        "tags":str(data_in_response["labels"])+" "+str(data_in_response["group_name"]),
                                        "url":str(devices.get_path_device()[0])}
                    else:
                        redes_cartel = {
                                        "idRed":str(data_in_response["group_name"])+"|"+str(devices.get_serial_device()[0]),
                                        "nombre":str(data_in_response["site"]),
                                        "tags":str(data_in_response["labels"])+" "+str(data_in_response["group_name"]),
                                        "url":str(devices.get_path_device()[0])}

                    estado = {
                                "serial":str(devices.get_serial_device()[0]),
                                "status":str(data_in_response["status"]),
                                "dashboard":str(devices.get_path_device()[0])
                            }
                    if datos not in self.data_ap:
                        self.data_ap.append(datos) 
                    if estado not in self.__status_device_array:
                        self.__status_device_array.append(estado)    
                    self.__connection_mongodb.get_mongodb_network().insert_one(redes_cartel)
            self.process_query_aruba_ap_offset()
            print("Total Aruba "+str(self.__total_devices_aruba))
            print("Total de datos en BD Aruba"+str(self.__conection_mysql_db.verify_total_devices_in_dashboards("Aruba",self.__total_devices_aruba)))
            return True         
        except Exception as ex:
            print("Error "+str(ex))
            self.generate_new_token_aruba_dashboard()
            return False

    def process_query_aruba_ap_offset(self):
        try:
            for data_in_response in range(1000,self.__offset,1000):
                response_data =  self.generate_query_aps_to_json(False,data_in_response)
                if "message" not in response_data:
                    for data_in_response in response_data["aps"]:
                        devices = dev.Devices(str(data_in_response["serial"]).strip(),str(data_in_response["name"]).strip(),
                                          str(data_in_response["ip_address"]),str(data_in_response["macaddr"]),
                                          str(data_in_response["model"]),str(data_in_response["notes"]),
                                          "AP","ARUBA","ARUBA")
                        datos = {
                            "serial":str(devices.get_serial_device()[0]),
                            "name":str(devices.get_name_device()[0]),
                            "lanIp":str(devices.get_lanip_device()[0]),
                            "mac":str(devices.get_macaddress_device()[0]),
                            "model":str(devices.get_model_device()[0]),
                            "notes":str(devices.get_notes_device()[0]),
                            "tags":[str(devices.get_path_device()[0]), "AP"],
                            "url": str(devices.get_path_device()[0])
                        }
                        if data_in_response["site"] == None:
                            redes_cartel = {
                                        "idRed":str(devices.get_name_device()[0])+"|"+str(devices.get_serial_device()[0]),
                                        "nombre":str(data_in_response["group_name"]),
                                        "tags":str(data_in_response["labels"])+" "+str(data_in_response["group_name"]),
                                        "url":str(devices.get_path_device()[0])}
                        else:
                            redes_cartel = {
                                        "idRed":str(data_in_response["group_name"])+"|"+str(devices.get_serial_device()[0]),
                                        "nombre":str(data_in_response["site"]),
                                        "tags":str(data_in_response["labels"])+" "+str(data_in_response["group_name"]),
                                        "url":str(devices.get_path_device()[0])}

                        estado = {
                                "serial":str(devices.get_serial_device()[0]),
                                "status":str(data_in_response["status"]),
                                "dashboard":str(devices.get_path_device()[0])
                            }
                        if datos not in self.data_ap:
                            self.data_ap.append(datos) 
                        if estado not in self.__status_device_array:
                            self.__status_device_array.append(estado) 
                    self.__connection_mongodb.get_mongodb_network().insert_one(redes_cartel)
            self.__total_devices_aruba += len(self.data_ap)
            self.__connection_mongodb.get_mongodb_devices_temporal().insert_many(self.data_ap)
            time.sleep(5)
            self.__connection_mongodb.get_mongodb_status_device_temporal().insert_many(self.__status_device_array) 
            return True
        except Exception as ex:
            print("Error offset"+str(ex))
            self.generate_new_token_aruba_dashboard()
            return False

    def get_format_aruba_gateway_name(self,name):
        print(name)
        if name.startswith("R"):
            data2 = name.split("-")
            if(len(data2[1]) < 4):
                print(str(data2[1]+str(len(data2[1]))))
                
    def process_query_aruba_gateways(self):
        try:
            self.__total_devices_aruba =0
            data =[]
            estado_array = []
            PATH_ARUBA_GATEWAYS = config.ARUBA_BASE_URL+config.ARUBA_URL_SEARCH_GATEWAYS
            HEADER_QUERY_ARUBA = {"Authorization":f"bearer "+self.__USER_ARUBA}
            SEND_QUERY_ARUBA_GATEWAYS = request.get(PATH_ARUBA_GATEWAYS,headers=HEADER_QUERY_ARUBA)
            response_query_to_json =  SEND_QUERY_ARUBA_GATEWAYS.json()
            if "message" not in response_query_to_json:
                for data_in_response in response_query_to_json["gateways"]:
                    #self.Format_GatewayName(str(i["name"]))
                    datos = {
                            "serial":str(data_in_response["serial"]),
                            "name":str(data_in_response["name"]),
                            "lanIp":"10.10.10.1 ",
                            "mac":str(data_in_response["macaddr"]),
                            "model":str(data_in_response["model"]),
                            "notes":"",
                            "tags":[str(data_in_response["labels"])+" ARUBA ROUTER"],
                            "url":"ARUBA"
                        }
                    if data_in_response["site"] == None:
                        
                        redes_cartel = {
                                        "idRed":str(data_in_response["name"])+"|"+str(data_in_response["serial"]),
                                        "nombre":str(data_in_response["group_name"]),
                                        "tags":str(data_in_response["labels"])+" "+str(data_in_response["group_name"]),
                                        "url":"ARUBA"}
                    else:
                        redes_cartel = {
                                         "idRed":str(data_in_response["group_name"])+"|"+str(data_in_response["serial"]),
                                         "nombre":str(data_in_response["site"]),
                                         "tags":str(data_in_response["labels"])+" "+str(data_in_response["group_name"]),
                                         "url":"ARUBA"}
                    estado = {"serial":str(data_in_response["serial"]),"status":str(data_in_response["status"]),"dashboard":"ARUBA"}
                    cantidad = self.__connection_mongodb.get_mongodb_devices_temporal().count_documents({"serial": str(data_in_response["serial"])})
                    if cantidad ==  0:
                        data.append(datos)
                    estado_array.append(estado)
                    self.__connection_mongodb.get_mongodb_network().insert_one(redes_cartel)
            self.__total_devices_aruba += len(data)
            self.__connection_mongodb.get_mongodb_devices_temporal().insert_many(data)
            time.sleep(5)
            self.__connection_mongodb.get_mongodb_status_device_temporal().insert_many(estado_array)                    
            return True
        except Exception as ex:
            print(str(ex))
            self.generate_new_token_aruba_dashboard()
            return False

        


