import time
from concurrent.futures import ThreadPoolExecutor
import config
import ArchivosAruba.var_aruba as var_aruba
import requests as request
import datetime
import telegram
import BaseDeDatos.Conexion_BD as Bd
import mongoScript as mongodb
import Models.Devices as dev
import Models.DeviceStatus as status_devices
import Models.NetworkCartel as network_cartel
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
                    data_device_aruba_switch = dev.Devices(str(i["serial"]),str(i["name"]),
                                                           str(i["ip_address"]),str(i["macaddr"]),
                                                           str(i["model"]),"",
                                                           ["ARUBA SWITCH"],"ARUBA","ARUBA")
                    network_cartel_format = network_cartel.NetworkCartel(str(i["serial"]),str(i["labels"]),"ARUBA")
                    if i["site"] == None:
                        network_cartel_format.set_network_name(str(i["name"]))
                        network_cartel_format.set_network_group_name(str(i["group_name"]))
                    else:
                        network_cartel_format.set_network_group_name(str(i["group_name"]))
                        network_cartel_format.set_network_site_name(str(i["site"]))
                    status_data = status_devices.DeviceStatus(str(i["serial"]),str(i["status"]),config.NAME_DASHBOARD_ARUBA)
                    status_format = status_data.get_format_save_device_data()
                    total_devices_in_database_from_serial = self.__connection_mongodb.get_mongodb_devices_temporal().count_documents({"serial": str(i["serial"])})
                    if  total_devices_in_database_from_serial == 0 :
                        data_device_switch.append(data_device_aruba_switch.get_format_save_device_data())
                    estado_array.append(status_format)
                    self.__connection_mongodb.get_mongodb_network().insert_one(network_cartel_format.get_format_save_device_data())
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
                    network_cartel_format = network_cartel.NetworkCartel(str(devices.get_serial_device()[0]),str(data_in_response["labels"]),config.NAME_DASHBOARD_ARUBA)
                    if data_in_response["site"] == None:
                        network_cartel_format.set_network_name(str(devices.get_name_device()[0]))
                        network_cartel_format.set_network_group_name(str(data_in_response["group_name"]))
                    else:
                        network_cartel_format.set_network_group_name(str(data_in_response["group_name"]))
                        network_cartel_format.set_network_site_name(str(data_in_response["site"]))
                    status_data = status_devices.DeviceStatus(str(devices.get_serial_device()[0]),str(data_in_response["status"]),str(devices.get_path_device()[0]))
                    status_format = status_data.get_format_save_device_data()
                    datos = devices.get_format_save_device_data()
                    if datos not in self.data_ap:
                        self.data_ap.append(datos) 
                    if status_format not in self.__status_device_array:
                        self.__status_device_array.append(status_format)    
                    self.__connection_mongodb.get_mongodb_network().insert_one(network_cartel_format.get_format_save_device_data())
            self.process_query_aruba_ap_offset()
            print("Total Aruba "+str(self.__total_devices_aruba))
            print("Total de datos en BD Aruba"+str(self.__conection_mysql_db.verify_total_devices_in_dashboards(config.NAME_DASHBOARD_ARUBA,self.__total_devices_aruba)))
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
                        network_cartel_format = network_cartel.NetworkCartel(str(devices.get_serial_device()[0]),str(data_in_response["labels"]),str(devices.get_path_device()[0]))
                        if data_in_response["site"] == None:
                            network_cartel_format.set_network_name(str(devices.get_name_device()[0]))
                            network_cartel_format.set_network_group_name(str(data_in_response["group_name"]))
                        else:
                            network_cartel_format.set_network_group_name(str(data_in_response["group_name"]))
                            network_cartel_format.set_network_site_name(str(data_in_response["site"]))

                        status_data = status_devices.DeviceStatus(str(devices.get_serial_device()[0]),str(data_in_response["status"]),str(devices.get_path_device()[0]))
                        status_format = status_data.get_format_save_device_data()

                        device_data_format = devices.get_format_save_device_data()

                        if device_data_format not in self.data_ap:
                            self.data_ap.append(device_data_format) 
                        if status_format not in self.__status_device_array:
                            self.__status_device_array.append(status_format) 
                    self.__connection_mongodb.get_mongodb_network().insert_one(network_cartel_format.get_format_save_device_data())
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
                    devices_gateways_data = dev.Devices(str(data_in_response["serial"]),str(data_in_response["name"]),
                                          "10.10.10.1",str(data_in_response["macaddr"]),
                                          str(data_in_response["model"]),"",
                                          [str(data_in_response["labels"])+" ARUBA ROUTER"],"ARUBA","ARUBA")
                    network_cartel_format = network_cartel.NetworkCartel(str(devices_gateways_data.get_serial_device()[0]),str(data_in_response["labels"]),str(devices_gateways_data.get_path_device()[0]))   
                    if data_in_response["site"] == None:
                        network_cartel_format.set_network_name(str(devices_gateways_data.get_name_device()[0]))
                        network_cartel_format.set_network_group_name(str(data_in_response["group_name"]))
                    else:
                        network_cartel_format.set_network_group_name(str(data_in_response["group_name"]))
                        network_cartel_format.set_network_site_name(str(data_in_response["site"]))
                    status = status_devices.DeviceStatus(str(data_in_response["serial"]),str(data_in_response["status"]),config.NAME_DASHBOARD_ARUBA)
                    cantidad = self.__connection_mongodb.get_mongodb_devices_temporal().count_documents({"serial": str(data_in_response["serial"])})
                    if cantidad ==  0:
                        data.append(devices_gateways_data.get_format_save_device_data())
                    estado_array.append(status.get_format_save_device_data())
                    self.__connection_mongodb.get_mongodb_network().insert_one(network_cartel_format.get_format_save_device_data())
            self.__total_devices_aruba += len(data)
            self.__connection_mongodb.get_mongodb_devices_temporal().insert_many(data)
            time.sleep(5)
            self.__connection_mongodb.get_mongodb_status_device_temporal().insert_many(estado_array)                    
            return True
        except Exception as ex:
            print(str(ex))
            self.generate_new_token_aruba_dashboard()
            return False

        


