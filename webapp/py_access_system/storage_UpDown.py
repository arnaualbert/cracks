import subprocess
from controllers.login_controller import get_connection
from flask import Flask, render_template, request, redirect, session
import os
from py_access_system.plantilla_docker_compose import create_docker_compose_template
import re
import json

#comintario


# def "arnau":
#     return os.getlogin()

def get_path_user(username):
    current_user = "arnau"
    file_path = f"/home/{current_user}/users_storage/{username}"
    return file_path



def extract_paths(data, current_path=""):
    paths = {
        "directories": [],
        "files": []
    }
    for item in data:
        if item["type"] == "directory":
            dir_path = f"{current_path}/{item['name']}".replace("//", "/")
            # paths["directories"].append(dir_path)
            if "contents" in item:
                sub_paths = extract_paths(item["contents"], dir_path)
                paths["directories"].extend(sub_paths["directories"])
                paths["files"].extend(sub_paths["files"])
        elif item["type"] == "file":
            file_path = f"{current_path}/{item['name']}".replace("//", "/")
            paths["files"].append(file_path)
    return paths

# def extract_paths(data, current_path=""):
#     paths = {}
#     for item in data:
#         if item["type"] == "directory":
#             dir_path = f"{current_path}/{item['name']}".replace("//", "/")
#             paths[dir_path] = []
#             if "contents" in item:
#                 sub_paths = extract_paths(item["contents"], dir_path)
#                 paths.update(sub_paths)
#         elif item["type"] == "file":
#             file_path = f"{current_path}/{item['name']}".replace("//", "/")
#             if current_path in paths:
#                 paths[current_path].append(file_path)
#             else:
#                 paths[current_path] = [file_path]
#     return paths


# def extract_paths(data, current_path=""):
#     paths = {}
#     for item in data:
#         if item["type"] == "directory":
#             dir_path = f"{current_path}/{item['name']}".replace("//", "/")
#             paths[dir_path] = {"files": [], "directories": {}}
#             if "contents" in item:
#                 sub_paths = extract_paths(item["contents"], dir_path)
#                 paths[dir_path]["directories"].update(sub_paths)
#         elif item["type"] == "file":
#             file_path = f"{current_path}/{item['name']}".replace("//", "/")
#             if current_path not in paths:
#                 paths[current_path] = {"files": [], "directories": {}}
#             paths[current_path]["files"].append(file_path)
#     return paths


def get_all_from_user(username):
    path = get_path_user(username)
    output = subprocess.check_output(["tree",path,"-J"])
    paths = extract_paths(json.loads(output.decode()))
    print(paths)
    return paths


#creamos un espacio para el usurio sino esta creado
def crear_user_espacio():
    username = session.get("username")
    file_path = get_path_user(username)
    
    # verficamos si la carpeta del usuario no existe, sino la creamos
    if not os.path.exists(file_path):
        try:
            os.makedirs(file_path)
            print(f"Directorio '{file_path}' creado correctamente.")
            #insert_db()
        except Exception as e:
            print(f"Error al crear el directorio: {e}")
    else:
        print(f"El directorio '{file_path}' ya existe.")

def crear_carpeta(folder_name, user_name):    
    user_path = get_path_user(username=user_name)
    folder_path = os.path.join(user_path, folder_name)
    
    try:
        os.makedirs(folder_path)
        print(f"Carpeta '{folder_name}' creada correctamente en '{user_path}'.")
    except FileExistsError:
        print(f"La carpeta '{folder_name}' ya existe en '{user_path}'.")
    except Exception as e:
        print(f"Error al crear la carpeta '{folder_name}': {e}")

def subir_carpeta():
    pass

def subir_fichero():
    pass

def insert_db():
    pass