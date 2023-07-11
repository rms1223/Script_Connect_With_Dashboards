import mongoScript as mongodb

con_mongo = mongodb.Mongo_Database()
import BaseDeDatos.Conexion_BD as Bd
datos_db = Bd.MysqlDb()

class InventoryDevices:

    def __init__(self) -> None:
        self.data_dict={}
        self.code_models ={}
        self.data = con_mongo.get_mongodb_devices().find({})
        self.data_tem = datos_db.get_codes_models()

    def list_code_models(self):
        for code_model in self.data_tem:
            self.code_models[code_model[1]] = code_model[0]

    def list_devices_models_from_database(self):
        for model_device in self.data:
            val = self.code_models.get(model_device['model'])
            if val not in self.data_dict.keys():
                self.data_dict[val] = 1
            else:
                val_temp = self.data_dict[val]
                self.data_dict[val] = val_temp + 1

    def save_data_inventory_in_database(self):
        for register in self.data_dict:
            datos_db.insert_total_devices_in_dasboards((register,self.data_dict[register]))
            print(f"{str(register)} ------- {str(self.data_dict[register])}")

    def init_process_inventory(self):
        self.list_code_models()
        self.list_devices_models_from_database()
        self.save_data_inventory_in_database()
        



