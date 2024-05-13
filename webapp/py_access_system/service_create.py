import subprocess
from controllers.login_controller import get_connection
from flask import Flask, render_template, request, redirect, session
import os
import own_env
from py_access_system.plantilla_docker_compose import create_docker_compose_template
import re

#comintario


def get_current_user():
    return os.getlogin()

def get_local_ip_address():
    ip_add = subprocess.check_output(["ifconfig","br0"])
    ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', ip_add.decode())
    mask_match = re.search(r'mask (\d+\.\d+\.\d+\.\d+)', ip_add.decode())
    if ip_match and mask_match:
        ip = ip_match.group(1)
        return ip
    else:
        return None
    # try:
    #     result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
    #     ip_addresses = result.stdout.strip().split()
    #     return ip_addresses[0] if ip_addresses else None
    # except Exception as e:
    #     print(f"Error al obtener la dirección IP local: {e}")
    #     return None


def create_docker_compose(cms_type, cms_name, cms_db_user, cms_db_password, cms_root_password):
    #ahora lo que vamos a hacer es crear un directrio de trabajo donde vamos a levantar el docker compose
    # # # cms_type="wordpress"
    # # # cms_name="benhammou"
    # # # cms_db_user="mohamed"
    # # # cms_db_password="mohamed"
    # # # cms_root_password="mohamed"
    username = session.get("username")
    puerto_libre = get_puerto_libre()

    file_path=get_path(cms_name)
    try:
        os.makedirs(file_path, exist_ok=True)
        print(f"Directorio(s) '{file_path}' creado(s) correctamente.")
        
        # volume_db_path = os.path.join(file_path, "db_data")
        # volume_cms_path = os.path.join(file_path, "cms_data")
        # os.makedirs(volume_db_path, exist_ok=True)
        # os.makedirs(volume_cms_path, exist_ok=True)
    except Exception as e:
        print(f"Error al crear el directorio: {e}")
    
    docker_compose_content = create_docker_compose_template(username, cms_type, cms_name, cms_db_user, cms_db_password, cms_root_password, puerto_libre)
    docker_compose_file = os.path.join(file_path, "docker-compose.yml")

    try:
        with open(docker_compose_file, "w") as f:
            f.write(docker_compose_content)
        print(f"Archivo Docker Compose '{docker_compose_file}' creado correctamente.")
    except Exception as e:
        print(f"Error al escribir el archivo Docker Compose: {e}")
    
    path_file_docker_compose=f"{file_path}/docker-compose.yml"
  
    return path_file_docker_compose

def get_path(cms_name):
    username = session.get("username")
    current_user = get_current_user()
    file_path = f"/home/{current_user}/docker/{cms_name}-{username}"
    return file_path

def create_cms(path_docker_compose,username, cms_type, cms_name, cms_db_user, cms_db_password, cms_root_password):
    original_directory = os.getcwd()
    try:
        # Obtenemos la contraseña del administrador
        #passw = own_env.getenv("PASSWORD_ROOT")


        # Cambiar al directorio donde se encuentra el archivo Docker Compose
        os.chdir(os.path.dirname(path_docker_compose))

        # Ejecutar el comando docker-compose
        command = f"""docker compose create"""
        subprocess.run(command, shell=True, check=True)
        print("Docker Compose levantado exitosamente.")

        os.chdir(original_directory)  

        puerto=get_puerto_libre()
        local_ip_address = get_local_ip_address()
        state="created"


        insert_service(username, cms_type, cms_name, cms_db_user, cms_db_password, cms_root_password,local_ip_address, puerto, state)
    except Exception as e:
        print(f"Error al levantar Docker Compose: {e}")
    
def insert_service(username:str ,cms_type:str, cms_name:str, cms_db_user:str, cms_db_password:str, cms_root_password:str, ip:str, puerto:int, state:str):
    print("ha llegado aquí")
    conn = get_connection()
    cur = conn.cursor()
    print("ha llegado aquí1")
    cur.execute("INSERT INTO user_services (service_name, cms_type, cms_db_user, cms_db_password, cms_root_password, ip, puerto, state, username) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (cms_name, cms_type, cms_db_user, cms_db_password, cms_root_password, ip, puerto, state, username))
    conn.commit()
    conn.close()
    print("ha llegado aquí2")

# def get_puerto_libre():
#     conn = get_connection()
#     cur = conn.cursor()

#     # Consguimos los puertos ocupados en la tabla
#     cur.execute("SELECT puerto FROM user_services")
#     puertos_ocupados = [row[0] for row in cur.fetchall()]
#     conn.close()

#     # Buscamos el puerto libre más bajo dentro del rango
#     puerto_libre = None
#     for puerto in range(8081, 9001):
#         if puerto not in puertos_ocupados:
#             puerto_libre = puerto
#             break
#     return puerto_libre

def get_puerto_libre():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(puerto) FROM user_services")
    puerto_max= [row[0] for row in cur.fetchall()]
    print(puerto_max)
    conn.close()
    if puerto_max[0] is None or puerto_max[0] == "NULL":
        puerto_libre=8090
    else:
        puerto_libre= puerto_max[0]+1
    return puerto_libre