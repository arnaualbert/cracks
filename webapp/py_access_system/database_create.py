import os
import subprocess
from controllers.login_controller import get_connection
import os


def instert_into_databases_a_db(database_type,database_password,database_name,database_user,puerto, user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_databases(database_name,database_type,db_user,db_password,root_password,ip,puerto,username) VALUES (?,?,?,?,?,?,?,?)",
                    (database_name,database_type,database_user,database_password,database_password,"192.168.127.200",puerto,user))
    conn.commit()


def create_database(database_type,database_password,database_name,database_user,current_user):
    if database_type == "mariadb" or database_type == "mysql":
        original_directory = os.getcwd()
        puerto = get_puerto_libre()
        create_mdb_mysql(database_type,database_password,database_name,database_user,puerto)
        instert_into_databases_a_db(database_type,database_password,database_name,database_user,puerto, current_user)
        os.chdir(f"/home/arnau/Desktop/{database_name}")
        command = f"""docker compose up -d"""
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
      - /home/arnau/Desktop/{database_name}:/var/lib/mysql
"""

    directory_path = f"/home/arnau/Desktop/{database_name}"
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
    for puerto in range(3308, 4001):
        if puerto not in puertos_ocupados:
            puerto_libre = puerto
            break


    return puerto_libre

def get_databases(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_databases WHERE username = ?",
                    (user,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_current_user():
    return os.getlogin()

def get_path_db(database_name):
    current_user = get_current_user()
    file_path = f"/home/{current_user}/Desktop/{database_name}"
    return file_path

def database_delete(database_name):
    passw = os.getenv("PASSWORD_ROOT")
    original_directory = os.getcwd()
    path_docker_compose=get_path_db(database_name)

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
        delete_from_db_db(database_name)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def delete_from_db_db(database_name: str):

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM user_databases WHERE database_name=?", (database_name,))
    conn.commit()
    conn.close()


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