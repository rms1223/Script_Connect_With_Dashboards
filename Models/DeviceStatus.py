class DeviceStatus:
    def __init__(self, serial, status, dashboard) -> None:
        self.__serial = serial,
        self.__status = status,
        self.__dashboard = dashboard
        
    def get_serial_device(self):
        return self.__serial
    def get_status_device(self):
        return self.__status
    def get_dashboard_device(self):
        return self.__dashboard
    def get_format_save_device_data(self):
        return { "serial": self.__serial,
                "status": self.__status,
                "dashboard": self.__dashboard
            }