#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                              Aqui se asignan todas las variables Generales a compartir por los diferentes Script                                      #
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#------------------------------Archivos manejo de Errores-----------------------------------------#
arubaDevices_log = r"log_aruba_script.txt"
merakiDevices_log = r"log_meraki_script.txt"
merakiStatus_log = r"log_Estado_meraki_script.txt"
database_log = r"log_aruba_mysql.txt"
#------------------------------ARUBA Central Conexion---------------------------------------------#
client_id = ""
client_secret = ""
tipo ="refresh_token"
#------------------------------MERAKI Dashboard Conexion------------------------------------------#
id_org = ""
ips_reservadas = ["10.10.10.1","10.10.10.3","10.10.10.4","10.10.10.5","10.10.10.9"]
ips_server = ["10.10.10.3","10.10.10.4","10.10.10.5"]
carteles_sistema = ["2019-12","2020-01","2020-02"]
#------------------------------ARUBA-MERAKI-Data--------------------------------------------------#
dashboard_aruba = "ARUBA"
dashboard_meraki  = "MERAKI"
var_empty = ""
#------------------------------Base de datos------------------------------------------------------#
host = ""
user = ""
password = ""
database = ""
#------------------------------URL ARUBA----------------------------------------------------------#
url_refreshToken ="oauth2/token"
base_url_aruba = "https://apigw-prod2.central.arubanetworks.com/"
url_buscar_dispositivos = "monitoring/v1/gateways"
url_buscar_switch = "monitoring/v1/switches"
url_buscar_aps = "monitoring/v2/aps"
#------------------------------Bot token Telegram--------------------------------------------------#
bot_token_telegram = ""
chat_id_telegram = ""
#------------------------------Cantidad de Workers y tiempo de espera------------------------------#
workers = 2
espera = 420