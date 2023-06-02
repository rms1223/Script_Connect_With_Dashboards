#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                              Params to connect with diferentes dashboard and database                                                                 #
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------------- Files Errors ------------------------------------------------------------#
PATH_FILE_ERROR_ARUBA= r"error_aruba_script.txt"
PATH_FILE_ERROR_MERAKI = r"error_meraki_script.txt"
PATH_FILE_ERROR_STATUS_MERAKI = r"error_status_meraki_script.txt"
PATH_FILE_ERROR_MYSQLDB = r"error_mysql.txt"
PATH_FILE_ERROR_MONGODB = r"error_mongodb.txt"

#------------------------------------------------------------------------------------------- MERAKI --------------------------------------------------------------------#
IDS_ORGANIZATION_MERAKI = []
IPS_RESERVED = []
CARTELES_LICITACIONES = []
#------------------------------------------------------------------------------------------- Name Dashboard--------------------------------------------------------------#
NAME_DASHBOARD_ARUBA = "ARUBA"
NAME_DASHBOARD_MERAKI  = "MERAKI"
NAME_DASHBOARD_MERAKI_TYPE2  = "MERAKI2"
EMPTY_NAME = ""
#------------------------------------------------------------------------------------------ Params Database --------------------------------------------------------------#
MYSQL_HOST = ""
MYSQL_USER = ""
MYSQL_PASSWORD = ""
MYSQL_DATABASE = ""
#-------------------------------------------------------------------------------------------Params ARUBA ------------------------------------------------------------------#
ID_CLIENTE_ARUBA = ""
SECRET_CLIENT_ARUBA = ""
TYPE_ARUBA_TOKEN ="refresh_token"
ARUBA_NAME_ID = "client_id"
ARUBA_NAME_SECRET = "client_secret"
ARUBA_NAME_TYPE = "grant_type"
ARUBA_NAME_REFRESH_TOKEN = "refresh_token"
ARUBA_NAME_ACCESS_TOKEN = "access_token"
ARUBA_URL_REFRESH_TOKEN ="oauth2/token"
ARUBA_BASE_URL = "https://apigw-prod2.central.arubanetworks.com/"
ARUBA_URL_SEARCH_GATEWAYS = "monitoring/v1/gateways?limit=1000"
ARUBA_URL_SEARCH_SWITCH = "monitoring/v1/switches?limit=1000"
ARUBA_URL_SEARCH_APS = "monitoring/v2/aps?calculate_total=true&limit=1000"
#------------------------------------------------------------------------------------------Bot token Telegram ----------------------------------------------------------#
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
#------------------------------------------------------------------------------------------ Workers and wait time---------------------------------------#
PROCESS_WORKER = 2
PROCESS_WAIT = 300
PROCESS_WAIT_HUAWEI = 500
#------------------------------------------------------------------------------------------Huawei Credentials---------------------------------------------------------#
HUAWEI_USER = ""
HUAWEI_PASSWORD=""
HUAWEI_PATH_LOGIN = ""
HUAWEI_PATH_DEVICES = ""
HUAWEI_SELENIUM_PATH_DRIVER = r""
HUAWEI_PATH_DOWNLOAD_FILES  = r""
#------------------------------------------------------------------------------------------Params SDWAN CISCO-------------------------------------------------------------#
SDWAN_VMANAGE_HOST_PATH =""
SDWAN_BASE_URL = ""
SDWAN_URL_GET_TOKEN= "/dataservice/client/token"
SDWAN_URL_CHECKSESSIONID = "/j_security_check"
SDWAN_URL_GATEWAYS = "/dataservice/device"
SDWAN_URL_DEVICE_ID = "/dataservice/device/system/status?deviceId="
SDWAN_USER = ""
SDWAN_PASSWORD = ""
