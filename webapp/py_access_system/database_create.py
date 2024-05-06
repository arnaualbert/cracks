import os


def create_database(database_type):
    create_mdb_mysql()
    



def create_mdb_mysql(type,database_password,database_name,database_user):
    compose = f"""services:
  {type}:
    image: {type}
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



create_mdb_mysql("mariadb","a123","arnau","mohamed")


def create_postgress(database_name,database_user,database_password):
    compose = f"""
services:
  postgresql:
    image: postgres
    restart: always
    environment:
      POSTGRES_DB: {database_name}
      POSTGRES_USER: {database_user}
      POSTGRES_PASSWORD: {database_password}
    ports:
      - "5472:5432"
    volumes:
      - /home/arnau/Desktop/{database_name}/{database_name}:/var/lib/postgresql/data
"""
    pass