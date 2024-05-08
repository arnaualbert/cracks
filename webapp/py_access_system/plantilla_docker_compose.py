import subprocess
from controllers.login_controller import get_connection
import os
import own_env



def create_docker_compose_template(user_name,cms_type, cms_name, cms_db_user, cms_db_password, cms_root_password, puerto_libre):
    
    if cms_type=="wordpress":
        template = f'''
services:
  db:
    container_name: db_{cms_name}_{user_name}
    # We use a mariadb image which supports both amd64 & arm64 architecture
    image: mariadb:10.6.4-focal
    # If you really want to use MySQL, uncomment the following line
    #image: mysql:8.0.27

    command: '--default-authentication-plugin=mysql_native_password'
    volumes:
      - ./db_data:/var/lib/mysql
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
    container_name: wordpress_{cms_name}_{user_name}
    image: wordpress:latest
    volumes:
      - ./cms_data:/var/www/html
    ports:
      - {puerto_libre}:80
    restart: always
    environment:
      - WORDPRESS_DB_HOST=db
      - WORDPRESS_DB_USER={cms_db_user}
      - WORDPRESS_DB_PASSWORD={cms_db_password}
      - WORDPRESS_DB_NAME={cms_name}
volumes:
  db_data:
  cms_data:
'''
    elif cms_type=="drupal":
        template = f'''
services:
  db:
    container_name: db_{cms_name}_{user_name}
    image: mariadb:10.6.4-focal
    command: '--default-authentication-plugin=mysql_native_password'
    volumes:
      - ./db_data:/var/lib/mysql
      - ./init_scripts:/docker-entrypoint-initdb.d  # Monta los scripts de inicialización
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD={cms_root_password}
      - MYSQL_DATABASE={cms_name}
      - MYSQL_USER={cms_db_user}
      - MYSQL_PASSWORD={cms_db_password}
    expose:
      - 3306
      - 33060

  drupal:
    container_name: drupal_{cms_name}_{user_name}
    image: drupal:latest
    volumes:
      - ./cms_data:/var/www/html
      - ./init_scripts:/docker-entrypoint-initdb.d  # Monta los scripts de inicialización
    ports:
      - {puerto_libre}:80
    restart: always
    environment:
      - DRUPAL_DB_HOST=db
      - DRUPAL_DB_USER={cms_db_user}
      - DRUPAL_DB_PASSWORD={cms_db_password}
      - DRUPAL_DB_NAME={cms_name}

volumes:
  db_data:
  cms_data:
'''
    elif cms_type=="joomla":
        template = f'''
version: '3.1'
       
services:
  joomladb:
    container_name: joomladb_{cms_name}_{user_name}
    image: mysql:5.7
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD={cms_root_password}
    volumes:
      - ./db_data:/var/lib/mysql
  joomla:
    container_name: joomla_{cms_name}_{user_name}
    image: joomla
    restart: always
    ports:
      - {puerto_libre}:80
    environment:
      - JOOMLA_DB_HOST=joomladb
      - JOOMLA_DB_PASSWORD={cms_db_password}
    volumes:
      - ./cms_data:/var/www/html

volumes:
  db_data:
  cms_data:
'''
    elif cms_type=="prestashop":
        template = f'''       
services:
  mysql:
    container_name: db_{cms_name}_{user_name}
    image: mysql:5.7
    restart: unless-stopped
    environment:
      - MYSQL_ROOT_PASSWORD={cms_root_password}
      - MYSQL_DATABASE={cms_name}
    volumes:
      - ./db_data:/var/lib/mysql
    networks:
      - prestashop_network

  prestashop:
    container_name: prestashop_{cms_name}_{user_name}
    image: prestashop/prestashop:latest
    restart: unless-stopped
    depends_on:
      - mysql
    ports:
      - {puerto_libre}:80
    environment:
      - DB_SERVER=some-mysql
      - DB_NAME={cms_name}
      - DB_USER={cms_db_user}
      - DB_PASSWD={cms_db_password}
    volumes:
      - ./cms_data:/var/www/html
    networks:
      - prestashop_network

networks:
  prestashop_network:
    driver: bridge

volumes:
  db_data:
  cms_data:
'''
        
    return template
