import config
import datetime
import mongoScript as mongodb
#------------------------------------------------------------------- Se deshabilitan Los warnings de las consultas al SD WAN ------------------------------------------#
import requests as requests
from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ViptelaDevices:
    __conection_mongodb = mongodb.Mongo_Database()
    def __init__(self):
        pass

    #--------------------------------------------------------------------Metodo para obtener el Session ID SDWAN ----------------------------------------------------------#
    def get_jsessionid_sdwan_dashboard(self, username, password):
            PATH_VIPTELA_SESSION_ID = config.SDWAN_BASE_URL + config.SDWAN_URL_CHECKSESSIONID
            payload = {'j_username' : username, 'j_password' : password}

            RESPONSE_QUERY_VIPTELA_SESSIONID = requests.post(url=PATH_VIPTELA_SESSION_ID, data=payload, verify=False)
            try:
                cookies = RESPONSE_QUERY_VIPTELA_SESSIONID.headers["Set-Cookie"]
                jsessionid = cookies.split(";")
                return(jsessionid[0])
            except:
                print("No valid JSESSION ID returned\n")
                exit()

    def get_status_sdwan_dashboard(self,device_status):
        return "ONLINE" if device_status == "reachable" else "OFFLINE"
    #--------------------------------------------------------------------Metodo para obtener el Token SDWAN para la conexion -----------------------------------------------#
    def get_token_sdwan_dashboard(self,jsessionid):
        HEADER_QUERY_VIPTELA = {'Cookie': jsessionid}
        PATH_VIPTELA_TOKEN = config.SDWAN_BASE_URL + config.SDWAN_URL_GET_TOKEN      
        RESPONSE_QUERY_VIPTELA_GATEWAYS = requests.get(url=PATH_VIPTELA_TOKEN, headers=HEADER_QUERY_VIPTELA, verify=False)
        if RESPONSE_QUERY_VIPTELA_GATEWAYS.status_code == 200:
            return(RESPONSE_QUERY_VIPTELA_GATEWAYS.text)
        else:
            return None


    def get_viptela_query_header(self):
        __session_id = self.get_jsessionid_sdwan_dashboard(config.SDWAN_USER,config.SDWAN_PASSWORD)
        __token = self.get_token_sdwan_dashboard(__session_id)
        if __token is not None:
            __header = {'Content-Type': "application/json",'Cookie': __session_id, 'X-XSRF-TOKEN': __token}
        else:
            __header = {'Content-Type': "application/json",'Cookie': __session_id}
        return __header

    def process_devices_viptela(self,response_query_to_json):
        for data_in_response in response_query_to_json["data"]:
                try:
                    device_viptela_data = {
                            "serial":str(data_in_response['uuid']),
                            "name":str(data_in_response['host-name']),
                            "lanIp":str("10.10.10.1"),
                            "mac":str(data_in_response['board-serial']),
                            "model":str(data_in_response['device-model']),
                            "notes":"",
                            "tags":[str(data_in_response['site-id']),str(data_in_response['device-groups'])],
                            "url":"Cisco_VIPTELA"
                        }
                    network_viptela = {
                                    "idRed":str(data_in_response['host-name'])+"|"+str(data_in_response['uuid']),
                                    "nombre":str(data_in_response["site-id"]),
                                    "tags":[str(data_in_response['site-id']),str(data_in_response['device-groups'])],
                                    "url":"Cisco_VIPTELA"}
                    status_device_viptela = {
                                "serial":str(data_in_response['uuid']),
                                "status": self.get_status_sdwan_dashboard(str(data_in_response['reachability'])),
                                "dashboard":"Cisco_VIPTELA"
                            }
                    self.__conection_mongodb.get_mongodb_network().insert_one(network_viptela)
                    self.__conection_mongodb.get_mongodb_devices_temporal().insert_one(device_viptela_data)
                    self.__conection_mongodb.get_mongodb_status_device_temporal().insert_one(status_device_viptela)
                except Exception as ex:
                    print(f"Error {+str(ex)}")
            

    def start_process(self):
        try:
            PATH_VIPTELA_SWITCH = config.SDWAN_BASE_URL + config.SDWAN_URL_GATEWAYS     
            SEND_QUERY_VIPTELA_GATEWAYS = requests.get(url=PATH_VIPTELA_SWITCH, headers=self.get_viptela_query_header(), verify=False)
            response_query_to_json = SEND_QUERY_VIPTELA_GATEWAYS.json()
            self.process_devices_viptela(response_query_to_json)
        except Exception as ex:
            print(f"Error al procesar la Peticion SDWAN CISCO {str(ex)}")
        