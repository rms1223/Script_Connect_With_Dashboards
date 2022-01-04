class FormatterData:
    def initialize(self):
        pass
    def Get_Format_Gateway(self,data):
        return {
                "serial":str(data["serial"]),
                "name":str(data["name"]),
                "lanIp":"10.10.10.1 ",
                "mac":str(data["macaddr"]),
                "model":str(data["model"]),
                "notes":"",
                "tags":[str(data["labels"])+" ARUBA ROUTER"],
                "url":"ARUBA"
            }
    def Get_Format_Switch(self,data):
        return {
                "serial":str(data["serial"]),
                "name":str(data["name"]),
                "lanIp":str(data["ip_address"]),
                "mac":str(data["macaddr"]),
                "model":str(data["model"]),
                "notes":"",
                "tags":["ARUBA SWITCH"],
                "url":"ARUBA"
            }
    def Get_Format_Ap(self,data):
        return {
                "serial":str(data["serial"]),
                "name":str(data["name"]),
                "lanIp":str(data["ip_address"]),
                "mac":str(data["macaddr"]),
                "model":str(data["model"]),
                "notes":str(data["notes"]),
                "tags":["ARUBA AP"],
                "url":"ARUBA"
            }
    def Get_Format_RedesCartel_GroupName(self,data):
        return {
                "idRed":str(data["group_name"])+"|"+str(data["serial"]),
                "nombre":str(data["site"]),
                "tags":str(data["labels"])+" "+str(data["group_name"]),
                "url":"ARUBA"
            }
    def Get_Format_RedesCartel_Name(self,data):
        return {
                "idRed":str(data["name"])+"|"+str(data["serial"]),
                "nombre":str(data["group_name"]),
                "tags":str(data["labels"])+" "+str(data["group_name"]),
                "url":"ARUBA"
            }
    def Get_Format_Status(self,data):
        return {
                "serial_equipo":str(data["serial"]),
                "estado":str(data["status"]),
                "dashboard":"ARUBA"
            }
    def Get_Format_Client_Router(self,data,codigo_equipo,url):
        return {
                "serial":str(data['ip']+"-"+codigo_equipo),
                "nombre":str(data['manufacturer']+" "+codigo_equipo),
                "ip":str(data['ip']),
                "mac":str(data['mac']),
                "modelo":str(data['manufacturer']),
                "tags":"ROUTER "+codigo_equipo,
                "estado":str(data['status']),
                "codigo":codigo_equipo,
                "ruta":url
            }
    def Get_Format_Client_Print(self,data,codigo_equipo,url):
        return {
                "serial":str(data['ip']+"-"+codigo_equipo),
                "nombre":str(data['manufacturer']+" "+codigo_equipo),
                "ip":str(data['ip']),
                "mac":str(data['mac']),
                "modelo":str(data['manufacturer']),
                "tags":"IMPRESORAS "+codigo_equipo,
                "estado":str(data['status']),
                "codigo":codigo_equipo,
                "ruta":url
            }
    def Get_Format_Client_Server(self,data,codigo_equipo,url):
        return {
                "serial":str(data['ip']+"-"+codigo_equipo),
                "nombre":str(data['description']+" "+codigo_equipo),
                "ip":str(data['ip']),"mac":str(data['mac']),
                "modelo":str(data['manufacturer']),
                "tags":"SERVER "+codigo_equipo,
                "estado":str(data['status']),
                "codigo":codigo_equipo,
                "ruta":url
            }