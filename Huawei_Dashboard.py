from ast import With
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import csv
import os
import glob
from time import sleep, time
import config
import mongoScript as mongodb
import Models.Devices as dev
import Models.DeviceStatus as status_devices
import Models.NetworkCartel as network_cartel
CONNECTION_MONGODB = mongodb.Mongo_Database()
import BaseDeDatos.Conexion_BD as Bd
CONNECTION_MYSQL = Bd.MysqlDb()

class HuaweiDevices:
    
    def __init__(self) -> None:
        pass


    def imaster_huawei_csv_devices(self):
        selenium_chrome_options = webdriver.ChromeOptions()
        selenium_browser = webdriver.Chrome(config.HUAWEI_SELENIUM_PATH_DRIVER,chrome_options=selenium_chrome_options)
        selenium_browser.maximize_window()
        selenium_browser.get(config.HUAWEI_PATH_LOGIN)
        username_huawei_pagelogin = selenium_browser.find_element(By.ID,"username")
        password_huawei_pagelogin = selenium_browser.find_element(By.ID,"value")
        username_huawei_pagelogin.send_keys(config.HUAWEI_USER)
        password_huawei_pagelogin.send_keys(config.HUAWEI_PASSWORD)

        button_huawei_pagelogin =  WebDriverWait(selenium_browser, 40).until(EC.presence_of_element_located((By.ID,'submitDataverify')))
        button_huawei_pagelogin.click()
        sleep(5)

        selenium_browser.get(config.HUAWEI_PATH_DEVICES)
        button_huawei_page_pass = WebDriverWait(selenium_browser, 40).until(EC.element_to_be_clickable((By.ID,'uNaviWalkthroughBtns')))
        button_huawei_page_pass.click()
        button_huawei_page_pass2= WebDriverWait(selenium_browser, 40).until(EC.presence_of_element_located((By.XPATH,'//*[@id="deviceInfo_button_export"]')))
        button_huawei_page_pass2.click()

        selenium_browser.find_element(By.ID,"MessageDialog_0_1").click()
        sleep(5)
        selenium_browser.close()

    def get_list_path_csv_files_huawei(self):
        try:
            list_of_files = filter( os.path.isfile,
                            glob.glob(config.HUAWEI_PATH_DOWNLOAD_FILES + '*deviceInfo.csv'))
            list_of_files = sorted( list_of_files,
                            key = os.path.getmtime)
            return list_of_files[len(list_of_files)-1]
        except Exception as e:
            print(f"Error {str(e)}")
        


    def read_huawei_devices_from_file(self):
        try:
            status_device_array =[]
            data_device_huawei =[]
            paths_file_csv = self.get_list_path_csv_files_huawei()
            is_first_iteraction = True
            with open(paths_file_csv,newline="",encoding='Latin1') as File:  
                reader_file = csv.reader(File)
                for row_file in reader_file:
                    name_device = str(row_file[15])
                    status = str(row_file[6])
                    status_device = "offline" if ( status.strip() == "Offline") else "online"
                    ip_Router = "10.10.10.1" if ( name_device == "Gateway") else str(row_file[11]) 
                    devices = dev.Devices(str(row_file[0]).strip(),str(row_file[1]).strip(),ip_Router.strip(),str(row_file[12]).strip(),str(row_file[8]).strip(),str(row_file[4]).strip(),str(row_file[17]).strip(),str(row_file[15]).strip(),str(row_file[17]).strip())
                    device_huawei_data = devices.get_format_save_device_data()

                    status_data = status_devices.DeviceStatus(str(devices.get_serial_device()[0]),status_device,str(row_file[17]).strip())
                    status_device_huawei = status_data.get_format_save_device_data()
                    network_cartel_format = network_cartel.NetworkCartel(str(devices.get_serial_device()[0]),str(devices.get_notes_device()[0]),str(devices.get_path_device()[0]))
                    network_cartel_format.set_network_name(str(devices.get_name_device()[0]))
                    network_cartel_format.set_network_group_name(str(devices.get_name_device()[0]))
                    if is_first_iteraction:
                        is_first_iteraction = False
                        pass
                    else:
                        data_device_huawei.append(device_huawei_data)
                    status_device_array.append(status_device_huawei)
                    CONNECTION_MONGODB.get_mongodb_network().insert_one(network_cartel_format.get_format_save_device_data())

            print(str(len(data_device_huawei)))
            print("Total de datos en BD Huawei "+str(CONNECTION_MYSQL.verify_total_devices_in_dashboards(config.NAME_DASHBOARD_HUAWEI,len(data_device_huawei))))
            CONNECTION_MONGODB.get_mongodb_devices_temporal().insert_many(data_device_huawei)
            sleep(5)
            CONNECTION_MONGODB.get_mongodb_status_device_temporal().insert_many(status_device_array)
            os.remove(paths_file_csv)
        except Exception as e:
            print(f"Error:  {str(e)}")
              