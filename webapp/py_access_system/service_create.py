import subprocess
from controllers.login_controller import get_connection
from flask import Flask, render_template, request, redirect, session
import os
import own_env

def create_docker_compose(cms_type, cms_name, cms_db_user, cms_db_password, cms_root_password):
    docker_compose_content = create_docker_compose_template(cms_type, cms_name, cms_db_user, cms_db_password, cms_root_password)
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose_content)

def create_service():
    pass

def insert_service():
    pass


def create_docker_compose_template(cms_type, cms_name, cms_db_user, cms_db_password, cms_root_password):
    template = f'''
services:
  db:
    image: {"mariadb:10.6.4-focal" if cms_type == "mariadb" else "mysql:8.0.27"}
    command: '--default-authentication-plugin=mysql_native_password'
    volumes:
      - db_data:/var/lib/mysql
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD={cms_root_password}
      - MYSQL_DATABASE={cms_name}
      - MYSQL_USER={cms_db_user}
      - MYSQL_PASSWORD={cms_db_password}
    expose:
      - 3306
      - 33060
  wordpress:
    image: wordpress:latest
    volumes:
      - wp_data:/var/www/html
    ports:
      - 8083:80
    restart: always
    environment:
      - WORDPRESS_DB_HOST=db
      - WORDPRESS_DB_USER={cms_db_user}
      - WORDPRESS_DB_PASSWORD={cms_db_password}
      - WORDPRESS_DB_NAME={cms_name}
volumes:
  db_data:
  wp_data:
'''
    return template