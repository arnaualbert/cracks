from controllers.login_controller import get_connection
from py_access_system.service_create import get_path
import subprocess
import os
import os


def start_service(service_name):
    passw = os.getenv("PASSWORD_ROOT")
    original_directory = os.getcwd()
    path_docker_compose=get_path(service_name)

    try:
        # Cambiar al directorio donde se encuentra el archivo Docker Compose
        os.chdir(os.path.dirname(f"""{path_docker_compose}/docker-compose.yml"""))

        # Ejecutar el comando docker-compose
        command = f"""docker compose start"""
        subprocess.run(command, shell=True, check=True)
        print("Docker Compose lstarted successfully")
        
        os.chdir(original_directory) 
        estado="started"
        change_state_cms_in_db(service_name, estado)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def stop_service(service_name):
    passw = os.getenv("PASSWORD_ROOT")
    original_directory = os.getcwd()
    path_docker_compose=get_path(service_name)

    try:
        # Cambiar al directorio donde se encuentra el archivo Docker Compose
        os.chdir(os.path.dirname(f"""{path_docker_compose}/docker-compose.yml"""))

        # Ejecutar el comando docker-compose
        command = f"""docker compose stop"""
        subprocess.run(command, shell=True, check=True)
        print("Docker Compose stoped successfully")

        os.chdir(original_directory) 
        estado="stopped"
        change_state_cms_in_db(service_name, estado)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def change_state_cms_in_db(cms_name, state):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Actualizamos el estado del servicio en la base de datos
        cur.execute("UPDATE user_services SET state = ? WHERE service_name = ?", (state, cms_name))
        conn.commit()
        print("State updated successfully")
    except Exception as e:
        print(f"An error occurred while updating state: {e}")
    finally:
        conn.close()