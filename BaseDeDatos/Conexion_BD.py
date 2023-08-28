import config
from mysql.connector import (connection, Error)


class MysqlDb:
    def __init__(self):
        self.error_mysql_db = open(config.PATH_LOG_ERROR_MYSQLDB,"w")
    
    def connect_to_mysql(self):
        try:
            pool_conection = connection.MySQLConnection(
                host = config.MYSQL_HOST,
                user = config.MYSQL_USER,
                password = config.MYSQL_PASSWORD,
                database = config.MYSQL_DATABASE,
            )
            return pool_conection
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")

    def get_dashboard_refreshtoken_from_dashboard(self,dashboard_name):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __cursor = __connection_mysqldb.cursor()
            __sql_query = "SELECT refresh_token FROM token_access_dashboard WHERE nombre = '"+dashboard_name+"'"
            __cursor.execute(__sql_query)
            __rows = __cursor.fetchone()
            return __rows[0]
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()

    def get_dashboard_token_from_dashboard(self,dashboard_name):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __cursor = __connection_mysqldb.cursor()
            __sql_query = "SELECT token FROM token_access_dashboard WHERE nombre = '"+dashboard_name+"'"
            __cursor.execute(__sql_query)
            __rows = __cursor.fetchone()
            return __rows[0]
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()

    def update_dashboard_token(self,token,refresh_token,dashboard, date):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __cursor = __connection_mysqldb.cursor()
            __sql_query = "UPDATE token_access_dashboard SET token = '"+token+"', refresh_token = '"+refresh_token+"', fecha = '"+date+"' WHERE nombre = '"+dashboard+"'"
            __cursor.execute(__sql_query)
            __connection_mysqldb.commit()
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()

    def update_status_devices(self,serial, status):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __cursor = __connection_mysqldb.cursor()
            __sql_query = "UPDATE estado_dispositivos SET estado = %s WHERE serial_equipo = %s"
            __data_device = (status, serial)
            __cursor.execute(__sql_query, __data_device)
            __connection_mysqldb.commit()  
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()

    def insert_status_devices(self,device_status):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __cursor = __connection_mysqldb.cursor()
            __sql_query = "INSERT INTO estado_dispositivos VALUES(%s,%s,%s)"
            __cursor.execute(__sql_query, device_status)
            __connection_mysqldb.commit()
        except Error as mysql_error:
                self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()

    def get_total_devices(self,serial):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __cursor = __connection_mysqldb.cursor()
            __sql_query = "SELECT COUNT(*) FROM dispositivos_red WHERE serial = '"+serial+"'"
            __cursor.execute(__sql_query)
            __rows = __cursor.fetchone()
            return __rows[0]
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()

    def insert_networkdevices_in_mysql(self,device_data):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __cursor = __connection_mysqldb.cursor()
            __sql_query = "INSERT INTO dispositivos_red VALUES(%s,%s,%s,%s,%s,%s,%s)"
            __cursor.execute(__sql_query, device_data)
            __connection_mysqldb.commit()
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()

    def insert_network_in_mysql(self,data_network):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __cursor = __connection_mysqldb.cursor()
            __sql_query = "INSERT INTO redes VALUES(%s,%s,%s,%s)"
            __cursor.execute(__sql_query, data_network)
            __connection_mysqldb.commit()
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()
    
    def verify_network_from_id(self,id_network):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __sql_query = "SELECT count(*) from redes where idRed = %s"
            device_serial = (id_network,)
            __cursor = __connection_mysqldb.cursor()
            __connection_mysqldb.commit()
            __cursor.execute(__sql_query, device_serial)
            cursor_result = __cursor.fetchone()
            return cursor_result[0]
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()

    def verify_device_from_serial(self,device_serial):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __sql_query = "SELECT count(*) from estado_dispositivos where serial_equipo = %s"
            device_serial = (device_serial,)
            __cursor = __connection_mysqldb.cursor()
            __connection_mysqldb.commit()
            __cursor.execute(__sql_query, device_serial)
            cursor_result = __cursor.fetchone()
            return cursor_result[0]
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()

    def insert_template_from_network(self,data_template):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __cursor = __connection_mysqldb.cursor()
            __sql_query = "INSERT INTO template VALUES(%s,%s)"
            __cursor.execute(__sql_query, data_template)
            __connection_mysqldb.commit()
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()

    def update_template_from_network(self,code,template):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __cursor = __connection_mysqldb.cursor()
            __sql_query = "UPDATE template SET nombretemplate = '"+template+"' where codigoCe = '"+code+"'"
            __cursor.execute(__sql_query,)
            __connection_mysqldb.commit()
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()
            
    def get_totalcount_Template_from_code(self,code):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __cursor = __connection_mysqldb.cursor()
            __sql_query = "SELECT COUNT(*) FROM template WHERE codigoCe = '"+code+"'"
            __cursor.execute(__sql_query)
            rows = __cursor.fetchone()
            return rows[0]
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()

    def update_status_query_process(self,status):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __cursor = __connection_mysqldb.cursor()
            __sql_query = "UPDATE estado_db_registros SET estado = '"+status+"' WHERE idActualizacion = 001"
            __cursor.execute(__sql_query,)
            __connection_mysqldb.commit()
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()

    def verify_total_devices_in_dashboards(self,total,dashboard):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __sql_query = "SELECT count(*) from total_equipos_dashboards where dashboard = %s"
            dashboard_name = (dashboard,)
            __cursor = __connection_mysqldb.cursor()
            __connection_mysqldb.commit()
            __cursor.execute(__sql_query, dashboard_name)
            cursor_result = __cursor.fetchone()
            if cursor_result[0] == 0:
                self.insert_devices_in_dashoard((dashboard,total))
            else:
               self.update_total_devices_in_dashoard(dashboard,total) 
            return "Success"
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
            return "Error"
        finally:
            __cursor.close()
            __connection_mysqldb.close()

    def update_total_devices_in_dashoard(self,total,dashboard):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __cursor = __connection_mysqldb.cursor()
            __sql_query = f"UPDATE total_equipos_dashboards SET total = {total} WHERE dashboard = '{dashboard}'"
            __cursor.execute(__sql_query,)
            __connection_mysqldb.commit()
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()
    def insert_devices_in_dashoard(self,total_devices_in_dashboard):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __cursor = __connection_mysqldb.cursor()
            __sql_query = "INSERT INTO total_equipos_dashboards VALUES(%s,%s)"
            __cursor.execute(__sql_query, total_devices_in_dashboard)
            __connection_mysqldb.commit()
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()
    
    def verify_code_from_model(self,model):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __sql_query = "SELECT codigo_modelo FROM sistema_fod_cableado.modelos where modelo = %s"
            dashboard_name = (model,)
            __cursor = __connection_mysqldb.cursor()
            __connection_mysqldb.commit()
            __cursor.execute(__sql_query, dashboard_name)
            result = __cursor.fetchone()
            return result
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
            return "Error"
        finally:
            __cursor.close()
            __connection_mysqldb.close()

    def get_codes_models(self):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __sql_query = "SELECT codigo_modelo,modelo FROM sistema_fod_cableado.modelos"
            __cursor = __connection_mysqldb.cursor()
            __connection_mysqldb.commit()
            __cursor.execute(__sql_query)
            result = __cursor.fetchall()
            return result
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
            return "Error"
        finally:
            __cursor.close()
            __connection_mysqldb.close()
        
    def insert_total_devices_in_dasboards(self,total_devices):
        try:
            __connection_mysqldb = self.connect_to_mysql()
            __cursor = __connection_mysqldb.cursor()
            __sql_query = "INSERT INTO sistema_fod_cableado.cantidadequiposdashboard VALUES(%s,%s)"
            __cursor.execute(__sql_query, total_devices)
            __connection_mysqldb.commit()
        except Error as mysql_error:
            self.error_mysql_db.write("Error Process Query MYSQL "+str(mysql_error)+"\n")
        finally:
            __cursor.close()
            __connection_mysqldb.close()