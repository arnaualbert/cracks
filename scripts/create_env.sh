#!/bin/bash

sudo apt-get update
sudo apt install mariadb-server
sudo apt-get install libmariadb-dev
sudo apt install python3-pip
sudo apt install python3-flask
sudo apt install python3.10-venv
python3 -m venv venv
source venv/bin/activate
pip install Flask
pip install python-dotenv
pip install mariadb
pip install gunicorn
