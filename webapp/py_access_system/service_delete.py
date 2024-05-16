from controllers.login_controller import get_connection
from py_access_system.service_create import get_path
import subprocess
import os
import os
#import shutil


def delete_service(service_name):
    passw = os.getenv("PASSWORD_ROOT")
    original_directory = os.getcwd()
    path_docker_compose=get_path(service_name)

    try:
        # Cambiar al directorio donde se encuentra el archivo Docker Compose
        os.chdir(os.path.dirname(f"""{path_docker_compose}/docker-compose.yml"""))

        # Ejecutar el comando docker-compose
        command = f"""docker compose down"""
        subprocess.run(command, shell=True, check=True)
        print("Docker Compose deleted successfully.")

        # Eliminar el directorio que contiene el docker-compose.yaml
        command = f"echo '{passw}' | sudo -S rm -rf {path_docker_compose}"

        # Ejecutamos el comando
        subprocess.run(command, shell=True)
        print("Directory deleted successfully.")

        os.chdir(original_directory) 
        delete_from_db(service_name)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def delete_from_db(cms_name: str):

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM user_services WHERE service_name=?", (cms_name,))
    conn.commit()
    conn.close()