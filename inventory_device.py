import mongoScript as mongodb

con_mongo = mongodb.Mongo_Database()
import BaseDeDatos.Conexion_BD as Bd
datos_db = Bd.MysqlDb()

d={}
codigos_modelos ={}

data = con_mongo.get_mongodb_devices().find({})
data_tem = datos_db.get_codes_models()

for i in data_tem:
    codigos_modelos[i[1]] = i[0]
    
for data2 in data:
    #print(str(data2['model'])+"  --------   "+str(data2['name'])+"  --------   "+str(data2['url']))
    val = codigos_modelos.get(data2['model'])
    if val not in d.keys():
        d[val] = 1
    else:
        val_temp = d[val]
        d[val] = val_temp + 1

for registros in d:
    datos_db.insert_total_devices_in_dasboards((registros,d[registros]))
    print(str(registros)+" ------- "+str(d[registros]))





