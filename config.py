#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                             Params to connect with differents dashboards                                                                              #
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------------- Archivos manejo de Errores -----------------------------------------------#
PATH_LOG_ERROR_ARUBA= r"LogFiles//log_aruba_script.txt"
PATH_LOG_ERROR_MERAKI = r"LogFiles//log_meraki_script.txt"
PATH_LOG_ERROR_STATUS_MERAKI = r"LogFiles//log_status_meraki_script.txt"
PATH_LOG_ERROR_MYSQLDB = r"LogFiles//log_mysql.txt"
PATH_LOG_ERROR_MONGODB = r"LogFiles//log_mongodb.txt"
#-------------------------------------------------------------------------------------------- ARUBA --------------------------------------------------------------------#
ID_CLIENTE_ARUBA = ""
SECRET_CLIENT_ARUBA = ""
TYPE_ARUBA_TOKEN ="refresh_token"

ARUBA_NAME_ID = "client_id"
ARUBA_NAME_SECRET = "client_secret"
ARUBA_NAME_TYPE = "grant_type"
ARUBA_NAME_REFRESH_TOKEN = "refresh_token"
ARUBA_NAME_ACCESS_TOKEN = "access_token"
#------------------------------------------------------------------------------------------- MERAKI --------------------------------------------------------------------#
#id_org = "846353"
IDS_ORGANIZATION_MERAKI = []
IPS_RESERVED = []
CARTELES_LICITACIONES = []
#------------------------------------------------------------------------------------------- ARUBA-MERAKI --------------------------------------------------------------#
NAME_DASHBOARD_ARUBA = "ARUBA"
NAME_DASHBOARD_MERAKI  = "MERAKI"
NAME_DASHBOARD_MERAKI_TYPE2  = "MERAKI2"
NAME_DASHBOARD_HUAWEI  = "HUAWEI"
NAME_DASHBOARD_CISCO  = "CISCO_VIPTELA"
EMPTY_NAME = ""
#------------------------------------------------------------------------------------------ Base de datos --------------------------------------------------------------#
MYSQL_HOST = ""
MYSQL_USER = ""
MYSQL_PASSWORD = ""
MYSQL_DATABASE = ""
#-------------------------------------------------------------------------------------------URL ARUBA ------------------------------------------------------------------#
ARUBA_URL_REFRESH_TOKEN ="oauth2/token"
ARUBA_BASE_URL = "https://apigw-prod2.central.arubanetworks.com/"
ARUBA_URL_SEARCH_GATEWAYS = "monitoring/v1/gateways?limit=1000"
ARUBA_URL_SEARCH_SWITCH = "monitoring/v1/switches?limit=1000"
ARUBA_URL_SEARCH_APS = "monitoring/v2/aps?calculate_total=true&limit=1000"
#------------------------------------------------------------------------------------------Bot token Telegram ----------------------------------------------------------#
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
#------------------------------------------------------------------------------------------Cantidad de Workers y tiempo de espera---------------------------------------#
PROCESS_WORKER = 2
PROCESS_WAIT = 300
PROCESS_WAIT_HUAWEI = 500
#-------------------------------------------------------------------------------------------Credenciales Huawei---------------------------------------------------------#
HUAWEI_USER = ""
HUAWEI_PASSWORD=""
HUAWEI_PATH_LOGIN = "https://mx.naas.huaweicloud.com/unisso/login.action?decision=1&service=%2Funisess%2Fv1%2Fauth%3Fservice%3D%252F"
HUAWEI_PATH_DEVICES = "https://mx.naas.huaweicloud.com/campusNCE/campusNCEIndex.html#pageName=tenantConfigAssetDeviceList"
HUAWEI_SELENIUM_PATH_DRIVER = r""
HUAWEI_PATH_DOWNLOAD_FILES  = r""
#------------------------------------------------------------------------------------------SDWAN Parametros-------------------------------------------------------------#
SDWAN_VMANAGE_HOST_PATH ="vmanage-3501876.sdwan.cisco.com"
SDWAN_BASE_URL = "https://%s"%SDWAN_VMANAGE_HOST_PATH
SDWAN_URL_GET_TOKEN= "/dataservice/client/token"
SDWAN_URL_CHECKSESSIONID = "/j_security_check"
SDWAN_URL_GATEWAYS = "/dataservice/device"
SDWAN_URL_DEVICE_ID = "/dataservice/device/system/status?deviceId="
SDWAN_USER = ""
SDWAN_PASSWORD = ""
