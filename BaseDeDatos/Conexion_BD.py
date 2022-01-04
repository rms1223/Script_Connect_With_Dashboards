import config
from mysql.connector import (connection)


class ConexionBaseDeDatos:
    error = ""
    def __init__(self):
        self.error = open(config.database_log,"w")
    
    def ConectarMysql(self):
        try:
            pool_conection = connection.MySQLConnection(
                host = config.host,
                user = config.user,
                password = config.password,
                database = config.database,
            )
            return pool_conection
        except Exception as ex:
                print("Error al Procesar la peticion "+str(ex)+"\n")
                self.error.write("Error al Procesar la peticion "+str(ex)+"\n")
    

    def Get_Dashboard_RefreshToken(self,dashboard):
        try:
            conn = self.ConectarMysql()
            _cursor = conn.cursor()
            sql = "SELECT refresh_token FROM token_access_dashboard WHERE nombre = '"+dashboard+"'"
            _cursor.execute(sql)
            rows = _cursor.fetchone()

            _cursor.close()
            conn.close()
            
            return rows[0]
        except Exception as ex:
                print("Error al Procesar la peticion "+str(ex)+"\n")
                self.error.write("Error al Procesar la peticion "+str(ex)+"\n")
    def Get_Dashboard_token(self,dashboard):
        try:
            conn = self.ConectarMysql()
            _cursor = conn.cursor()
            sql = "SELECT token FROM token_access_dashboard WHERE nombre = '"+dashboard+"'"
            _cursor.execute(sql)
            rows = _cursor.fetchone()
            
            _cursor.close()
            conn.close()
            
            return rows[0]
        except Exception as ex:
                print("Error al Procesar la peticion "+str(ex)+"\n")
                self.error.write("Error al Procesar la peticion "+str(ex)+"\n")

    def Set_Dashboard_Tokens(self,token,refresh_token,dashboard):
        try:
            conn = self.ConectarMysql()
            _cursor = conn.cursor()
            sql = "UPDATE token_access_dashboard SET token = '"+token+"', refresh_token = '"+refresh_token+"' WHERE nombre = '"+dashboard+"'"
            _cursor.execute(sql)
            conn.commit()

            _cursor.close()
            conn.close()
        except Exception as ex:
                print("Error al Procesar la peticion "+str(ex))
                self.error.write("Error al Procesar la peticion "+str(ex)+"\n")

    #----------------------------------------------------------Metodos para guardar en la base de datos--------------------------------------#

    def Actualizar_Estado_Dispositivos(self,serial, estado):
        try:
            conn = self.ConectarMysql()
            cursor = conn.cursor()
            sql = "UPDATE estado_dispositivos SET estado = %s WHERE serial_equipo = %s"
            valores = (estado, serial)
            cursor.execute(sql, valores)
            conn.commit()

            cursor.close()
            conn.close()
            
        except Exception as ex:
            print("Error al Procesar la peticion- "+str(ex)+"\n")
            self.error.write("Error al Procesar la peticion- "+str(ex)+"\n")

    def Insertar_Estado_Dispositivos(self,valores):
        try:
            conn = self.ConectarMysql()
            cursor = conn.cursor()
            sql = "INSERT INTO estado_dispositivos VALUES(%s,%s,%s)"
            cursor.execute(sql, valores)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as ex:
            print("Error al Procesar la peticion- "+str(ex)+"\n")
            self.error.write("Error al Procesar la peticion- "+str(ex)+"\n")
    def Process_Get_Devices_Count(self,serial):
        try:
            conn = self.ConectarMysql()
            _cursor = conn.cursor()
            sql = "SELECT COUNT(*) FROM dispositivos_red WHERE serial = '"+serial+"'"
            _cursor.execute(sql)
            rows = _cursor.fetchone()
            _cursor.close()
            conn.close()
            return rows[0]
        except Exception as ex:
                print("Error al Procesar la peticion "+str(ex)+"\n")
                self.error.write("Error al Procesar la peticion "+str(ex)+"\n")

    def Insertar_Dispositivos(self,valores):
        try:
            conn = self.ConectarMysql()
            _cursor = conn.cursor()
            sql = "INSERT INTO dispositivos_red VALUES(%s,%s,%s,%s,%s,%s,%s)"
            _cursor.execute(sql, valores)
            conn.commit()
            _cursor.close()
            conn.close()
        except Exception as ex:
            print("Error al Procesar la peticion "+str(ex)+"\n")
            self.error.write("Error al Procesar la peticion "+str(ex)+"\n")

    def Insertar_Redes(self,valores):
        try:
            conn = self.ConectarMysql()
            _cursor = conn.cursor()
            sql = "INSERT INTO redes VALUES(%s,%s,%s,%s)"
            _cursor.execute(sql, valores)
            conn.commit()
            _cursor.close()
            conn.close()
        except Exception as ex:
            print("Error al Procesar la peticion..... "+str(ex)+"\n")
            self.error.write("Error al Procesar la peticion "+str(ex)+"\n")

    #-------------------------------------Metodos de Provenientes de Meraki---------------------------------------------
    
    def Verificar_Redes(self,idRed):
        try:
            conn = self.ConectarMysql()
            sql = "SELECT count(*) from redes where idRed = %s"
            serial = (idRed,)
            cur = conn.cursor()
            conn.commit()
            cur.execute(sql, serial)
            result = cur.fetchone()
            cur.close()
            conn.close()
            return result[0]
        except Exception as ex:
            print("Error al procesar los datos: "+str(ex)+"\n")
            self.error.write("Error al procesar los datos: "+str(ex)+"\n")

    def Verificar_Dispositivo(self,serial):
        try:
            conn = self.ConectarMysql()
            sql = "SELECT count(*) from estado_dispositivos where serial_equipo = %s"
            serial = (serial,)
            cur = conn.cursor()
            conn.commit()
            cur.execute(sql, serial)
            result = cur.fetchone()
            cur.close()
            conn.close()
            return result[0]
        except Exception as ex:
            print("Error al procesar los datos: "+str(ex)+"\n")
            self.error.write("Error al procesar los datos: "+str(ex)+"\n")

    def Insertar_Templates(self,valores):
        try:
            conn = self.ConectarMysql()
            cursor = conn.cursor()
            sql = "INSERT INTO template VALUES(%s,%s)"
            cursor.execute(sql, valores)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as ex:
            print("Error al Procesar la peticion- "+str(ex)+"\n")
            self.error.write("Error al Procesar la peticion- "+str(ex)+"\n")
    def Actualizar_Templates(self,codigo,template):
        try:
            conn = self.ConectarMysql()
            cursor = conn.cursor()
            sql = "UPDATE template SET nombretemplate = '"+template+"' where codigoCe = '"+codigo+"'"
            cursor.execute(sql,)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as ex:
            print("Error al Procesar la peticion- "+str(ex)+"\n")
            self.error.write("Error al Procesar la peticion- "+str(ex)+"\n")
    def Process_Get_CE_Template(self,codigo):
        try:
            conn = self.ConectarMysql()
            _cursor = conn.cursor()
            sql = "SELECT COUNT(*) FROM template WHERE codigoCe = '"+codigo+"'"
            _cursor.execute(sql)
            rows = _cursor.fetchone()
            _cursor.close()
            conn.close()
            return rows[0]
        except Exception as ex:
                print("Error al Procesar la peticion "+str(ex)+"\n")
                self.error.write("Error al Procesar la peticion "+str(ex)+"\n")

    def Actualizar_Estado_Proceso(self,estado):
        try:
            conn = self.ConectarMysql()
            _cursor = conn.cursor()
            sql = "UPDATE estado_db_registros SET estado = '"+estado+"' WHERE idActualizacion = 001"
            _cursor.execute(sql,)
            conn.commit()
            _cursor.close()
            conn.close()
        except Exception as ex:
                print("Error al Procesar la peticion "+str(ex)+"\n")
                self.error.write("Error al Procesar la peticion "+str(ex)+"\n")