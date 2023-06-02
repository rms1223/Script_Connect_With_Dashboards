class Devices:
    
    def __init__(self, serial,name,lanip,mac,model,notes,tags,url,manufacture):
        self.__serialDevice = serial,
        self.__namedevice = name,
        self.__lanIpDevice = lanip,
        self.__macDevice = mac,
        self.__modelDevice = model,
        self.__notesDevice = notes,
        self.__tagsDevice =  [tags,url],
        self.__urlDevices = manufacture,
    
    def get_serial_device(self):
        return self.__serialDevice
    def get_name_device(self):
        return self.__namedevice
    def get_lanip_device(self):
        return self.__lanIpDevice
    def get_macaddress_device(self):
        return self.__macDevice
    def get_model_device(self):
        return self.__modelDevice
    def get_notes_device(self):
        return self.__notesDevice
    def get_tags_device(self):
        return self.__tagsDevice
    def get_path_device(self):
        return self.__urlDevices