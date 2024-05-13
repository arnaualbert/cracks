import os
import subprocess
from controllers.login_controller import get_connection
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


def instert_into_databases_a_db(database_type,database_password,database_name,database_user,user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_databases(database_name,database_type,db_user,db_password,root_password,ip,puerto,username) VALUES (?,?,?,?,?,?,?,?,?)",
                    (database_name,database_type,database_password,database_name,database_user,user))
    conn.commit()


def create_database(database_type,database_password,database_name,database_user):
    if database_type == "mariadb" or database_type == "mysql":
        original_directory = os.getcwd()
        passw = getenv("PASSWORD_ROOT")
        puerto = get_puerto_libre()
        create_mdb_mysql(database_type,database_password,database_name,database_user,puerto)
        instert_into_databases_a_db()
        os.chdir(f"/home/mohamed/Desktop/{database_name}")
        command = f"""echo '{passw}' | sudo -S docker compose up -d"""
        subprocess.run(command, shell=True, check=True) 
        os.chdir(original_directory)



def create_mdb_mysql(database_type,database_password,database_name,database_user,puerto):
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
      - "{puerto}:3306"
    volumes:
      - /home/mohamed/Desktop/{database_name}/{database_name}:/var/lib/mysql
"""

    directory_path = f"/home/mohamed/Desktop/{database_name}"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    file_path = f"{directory_path}/docker-compose.yml"
    
    with open(file_path, "w") as file:
        file.write(compose)


def get_puerto_libre():
    conn = get_connection()
    cur = conn.cursor()

    # Consguimos los puertos ocupados en la tabla
    cur.execute("SELECT puerto FROM user_databases")
    puertos_ocupados = [row[0] for row in cur.fetchall()]
    conn.close()

    # Buscamos el puerto libre más bajo dentro del rango
    puerto_libre = None
    for puerto in range(3306, 4001):
        if puerto not in puertos_ocupados:
            puerto_libre = puerto
            break


    return puerto_libre



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
#       - /home/mohamed/Desktop/{database_name}/{database_name}:/var/lib/postgresql/data
# """
#     pass