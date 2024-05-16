import subprocess
from controllers.login_controller import get_connection
from flask import Flask, render_template, request, redirect, session
import os
from py_access_system.plantilla_docker_compose import create_docker_compose_template
import re

#comintario


def get_current_user():
    return os.getlogin()

def get_path_user(username):
    current_user = get_current_user()
    file_path = f"/home/{current_user}/users_storage/{username}"
    return file_path

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