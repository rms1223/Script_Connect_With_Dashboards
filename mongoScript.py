from pymongo import MongoClient

class Mongo_Database:

    def __init__(self):
        pass
    def Get_Connection_Object(self):
        self.client = MongoClient('localhost')
        return self.client.start_session()
    def Get_Connection(self):
        self.client = MongoClient('localhost')
        self.db =  self.client["dashboard_devices_status"]
        return self.db['devices_status']

    def Get_Connection_Network(self):
        self.client = MongoClient('localhost')
        self.db =  self.client["dashboard_devices_status"]
        return self.db['network_devices']

    def Get_Connection_Devices(self):
        self.client = MongoClient('localhost')
        self.db =  self.client["dashboard_devices_status"]
        return self.db['devices']

    def Get_Connection_template(self):
        self.client = MongoClient('localhost')
        self.db =  self.client["dashboard_devices_status"]
        return self.db['template']

    def Get_Connection_network_clients(self):
        self.client = MongoClient('localhost')
        self.db =  self.client["dashboard_devices_status"]
        return self.db['clients_in_networks']

    def Get_Count_Devices (self):
        return self.Get_Connection_Devices().count_documents({})

    def Get_Count_Devices_Status(self):
        return self.Get_Connection().count_documents({})

    def Get_Count_Networks(self):
        return self.Get_Connection_Network().count_documents({})

    def Get_Devices_CE(self,codigo):
        return self.Get_Connection_Devices().find({'name' : {'$regex' : '.*' + codigo + '.*'}})

    def Get_Devices_Serie(self,serie):
        return self.Get_Connection_Devices().count_documents({'serial' : serie}) #find_one({'serial' : serie}).
    def Get_Devices_Estado(self,serie):
        return self.Get_Connection().find_one({'serial_equipo' : serie})

    ###Buscar Nombre de la REd########
    def Get_Network_CE(self,codigo):
        return self.Get_Connection_Network().find_one({'tags' : {'$regex' : '.*' + codigo + '.*'}})

    ###Template
    def Get_Network_Template(self,id_temp):
        return self.Get_Connection_template().find_one({'id' : id_temp})
   
    ###
    def Get_Client_Id_Network(self,id):
        return self.Get_Connection_network_clients().count_documents({'serial' : id})

    