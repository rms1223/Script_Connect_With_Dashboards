import subprocess

# Iterable con las rutas de los scripts
scripts_paths = ("C:/Users/admincs/Desktop/ScriptDashboards/MerakiDevices.py", 
"C:/Users/admincs/Desktop/ScriptDashboards/ScriptEstadoEquiposAruba.py",
"C:/Users/admincs/Desktop/ScriptDashboards/StatusMerakiDevices.py")
try:
    __process = [subprocess.Popen(["python", script]) for script in scripts_paths]
    for data_process in __process:
        data_process.wait()
except Exception as ex:
    print(f"Error {ex}")

