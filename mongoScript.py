from pymongo import MongoClient

class Mongo_Database:

    def __init__(self):
        pass
    
    def get_mongodb_connection(self):
        self.client = MongoClient('localhost')
        return self.client.start_session()
    
    def get_mongodb_huawei_data(self):
        self.client = MongoClient('localhost')
        self.db =  self.client["dashboard_devices_status"]
        return self.db['huawei_data']
    
    def get_mongodb_devices_status(self):
        self.client = MongoClient('localhost')
        self.db =  self.client["dashboard_devices_status"]
        return self.db['devices_status']

    def get_mongodb_status_device_temporal(self):
        self.client = MongoClient('localhost')
        self.db =  self.client["dashboard_devices_status"]
        return self.db['devices_status_temp']

    def get_mongodb_network(self):
        self.client = MongoClient('localhost')
        self.db =  self.client["dashboard_devices_status"]
        return self.db['network_devices']
    
    def get_mongodb_viptela_Devices(self):
        self.client = MongoClient('localhost')
        self.db =  self.client["dashboard_devices_status"]
        return self.db['devices_sdwan']
      
    def get_mongodb_serial_viptela_devices(self):
        self.client = MongoClient('localhost')
        self.db =  self.client["dashboard_devices_status"]
        return self.db['devices_seriales_sdwan']

    def get_mongodb_devices(self):
        self.client = MongoClient('localhost')
        self.db =  self.client["dashboard_devices_status"]
        return self.db['devices']

    def get_mongodb_devices_temporal(self):
        self.client = MongoClient('localhost')
        self.db =  self.client["dashboard_devices_status"]
        return self.db['devices_temp']

    def get_mongodb_template(self):
        self.client = MongoClient('localhost')
        self.db =  self.client["dashboard_devices_status"]
        return self.db['template']

    def get_mongodb_network_clients(self):
        self.client = MongoClient('localhost')
        self.db =  self.client["dashboard_devices_status"]
        return self.db['clients_in_networks']
        
    def set_mongodb_information_centros_educativos(self):
        self.client = MongoClient('localhost')
        self.db =  self.client["dashboard_devices_status"]
        return self.db['geografiaCE']


    def get_mongodb_count_devices (self):
        return self.get_mongodb_devices().count_documents({})

    def get_mongodb_count_devices_status(self):
        return self.get_mongodb_devices_status().count_documents({})

    def get_mongodb_count_networks(self):
        return self.get_mongodb_network().count_documents({})

    def get_mongodb_devices_in_centros_educativos(self,code):
        return self.get_mongodb_devices().find({'name' : {'$regex' : '.*' + code + '.*'}})

    def get_monfogdb_serial_device(self,serial):
        return self.get_mongodb_devices().count_documents({'serial' : serial})
    
    def get_mongodb_device_status(self,serial):
        return self.get_mongodb_devices_status().find_one({'serial_equipo' : serial})
    
    def get_mongodb_network_name_from_code(self,code):
        return self.get_mongodb_network().find_one({'tags' : {'$regex' : '.*' + code + '.*'}})

    def get_mongodb_network_template_from_id(self,id_temp):
        return self.get_mongodb_template().find_one({'id' : id_temp})
   
    ###
    def get_mongodb_clients_from_idnetwork(self,id):
        return self.get_mongodb_network_clients().count_documents({'serial' : id})
    