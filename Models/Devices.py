class Devices:
    
    def __init__(self, serial,name,lanip,mac,model,notes,tags,url,manufacture):
        self.__serialDevice = serial,
        self.__namedevice = name,
        self.__lanIpDevice = lanip,
        self.__macDevice = mac,
        self.__modelDevice = model,
        self.__notesDevice = notes,
        self.__tagsDevice =  [str(tags),str(url)],
        self.__urlDevices = manufacture,
    
    def get_serial_device(self):
        return self.__serialDevice
    def get_name_device(self):
        return self.__namedevice[0]
    def get_lanip_device(self):
        return self.__lanIpDevice
    def get_macaddress_device(self):
        return self.__macDevice
    def get_model_device(self):
        return self.__modelDevice
    def get_notes_device(self):
        return self.__notesDevice[0]
    def get_tags_device(self):
        return self.__tagsDevice
    def get_path_device(self):
        return self.__urlDevices[0]
    def get_format_save_device_data(self):
        return {
                "serial":self.__serialDevice[0],
                "name":self.__namedevice[0],
                "lanIp":self.__lanIpDevice[0],
                "mac":self.__macDevice[0],
                "model":self.__modelDevice[0],
                "notes":self.__notesDevice[0],
                "tags":self.__tagsDevice[0],
                "url": self.__urlDevices[0]
            }
            
        
    
        