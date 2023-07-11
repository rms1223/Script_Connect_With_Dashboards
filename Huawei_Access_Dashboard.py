import datetime
import BaseDeDatos.Conexion_BD as Bd
import config
import time

import Huawei_Dashboard as Huawei
dash_huawei = Huawei.HuaweiDevices()


def ProcessHuawei():
    dash_huawei.imaster_huawei_csv_devices()


if __name__ == '__main__':
    while True:
        try:
            x = datetime.datetime.now()
            print(f"Script Huawei Iniciado...{str(x)}")
            ProcessHuawei()
            x = datetime.datetime.now()
            print(f"Script Huawei Finalizado...{str(x)}")
            time.sleep(config.PROCESS_WAIT)
        except Exception as ex:
            print(str(ex))
        
