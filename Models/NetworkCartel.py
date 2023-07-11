class NetworkCartel:
    def __init__(self,serial_device,network_tags,network_url) -> None:
        self.__serial = serial_device,
        self.__network_tags = network_tags,
        self.__network_url = network_url,
        self.__network_name = "no_data",
        self.__network_group_name = "no_data",
        self.__network_site_name = "no_data",
    
    def set_network_name(self, network_name="no_data"):
        self.__network_name = network_name
    def set_network_group_name(self, group_name="no_data"):
        self.__network_group_name = group_name
    def set_network_site_name(self, site_name="no_data"):
        self.__network_site_name = site_name 

    def get_format_save_device_data(self):
      if self.__network_site_name != "no_data":
          self.__network_name = self.__network_group_name
          self.__network_group_name = self.__network_site_name
      return {
                "idRed": f"{self.__network_name} | {self.__serial}",
                "nombre":self.__network_group_name,
                "tags":f"{self.__network_tags} | {self.__network_group_name}",
                "url": self.__network_url
            }