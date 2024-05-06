import os
import subprocess

import pathlib

def create_dict_env():
    file_env = pathlib.Path(".env").read_text().split()
    dict_env = {}
    for kv in file_env:
        list_kv = kv.split("=")
        dict_env[list_kv[0]] = list_kv[1]
    return dict_env


def getenv(key):
    dict_find = create_dict_env()
    return dict_find[key]

def create_database(database_type,database_password,database_name,database_user):
    if database_type == "mariadb" or database_type == "mysql":
        original_directory = os.getcwd()
        passw = getenv("PASSWORD_ROOT")
        create_mdb_mysql(database_type,database_password,database_name,database_user)
        os.chdir(f"/home/arnau/Desktop/{database_name}")
        command = f"""echo '{passw}' | sudo -S docker compose up -d"""
        subprocess.run(command, shell=True, check=True) 
        os.chdir(original_directory)
    # elif database_type == "postgress":
    #     pass



def create_mdb_mysql(database_type,database_password,database_name,database_user):
    compose = f"""services:
  {database_type}:
    image: {database_type}
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: {database_password}
      MYSQL_DATABASE: {database_name}
      MYSQL_USER: {database_user}
      MYSQL_PASSWORD: {database_password}
    ports:
      - "3376:3306"
    volumes:
      - /home/arnau/Desktop/{database_name}/{database_name}:/var/lib/mysql
"""

    directory_path = f"/home/arnau/Desktop/{database_name}"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)  # Create the directory if it doesn't exist

    file_path = f"{directory_path}/docker-compose.yml"
    
    with open(file_path, "w") as file:
        file.write(compose)



# create_database("mariadb","a1223","arnsau","mohamsed")


# def create_postgress(database_name,database_user,database_password):
#     compose = f"""
# services:
#   postgresql:
#     image: postgres
#     restart: always
#     environment:
#       POSTGRES_DB: {database_name}
#       POSTGRES_USER: {database_user}
#       POSTGRES_PASSWORD: {database_password}
#     ports:
#       - "5472:5432"
#     volumes:
#       - /home/arnau/Desktop/{database_name}/{database_name}:/var/lib/postgresql/data
# """
#     pass