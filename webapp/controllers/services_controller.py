from flask import Blueprint, request, render_template, redirect, make_response, session, jsonify
from controllers.login_controller import get_connection
from controllers.login_controller import check_is_logged
from py_access_system.service_create import create_docker_compose
from py_access_system.service_create import create_cms
from py_access_system.service_start import start_service 
from py_access_system.service_start import stop_service
from py_access_system.service_delete import delete_service

services_module = Blueprint('services_module', __name__, template_folder='templates')



@services_module.route("/services")
def user_services():
    username = session.get("username")
    if request.method == "GET" and check_is_logged():
        info_cms=select_services()
        return render_template("user_services.html",info=info_cms, username=username)
    else:
        return redirect("/login")

def select_services():
    info_services=[]
    username = session.get("username")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_services WHERE username = ?", (username,))
    rows = cursor.fetchall()
    if rows:
        for valor in rows:
            service_name = valor[0]
            cms_type = valor[1]
            cms_db_user = valor[2]
            cms_db_password = valor[3]
            cms_root_password = valor[4]
            ip = valor[5]
            puerto = valor[6]
            state = valor[7]
            info_services.append({
                "service_name": service_name,
                "cms_type": cms_type,
                "cms_db_user": cms_db_user,
                "cms_db_password": cms_db_password,
                "cms_root_password": cms_root_password,
                "ip": ip,
                "puerto": puerto,
                "state": state
            })

        conn.close()
        return info_services
    else:
        conn.close()
        return info_services


@services_module.route("/service_create", methods=["GET", "POST"])
def user_service_create():
    username = session.get("username")
    if request.method == "GET" and check_is_logged():
        return render_template("user_service_create.html", username=username)
    if request.method == "POST" and check_is_logged():

        cms_type = request.form.get("cmsType")
        cms_name = request.form.get("cmsNmae")
        cms_db_user= request.form.get("cmsdbUser")
        cms_db_password= request.form.get("cmsdbPassword")
        cms_root_password = request.form.get("cmsrootPassword")

        docker_compose_path = create_docker_compose(cms_type, cms_name, cms_db_user, cms_db_password, cms_root_password)
        
        username = session.get("username")
        create_cms(docker_compose_path, username,cms_type, cms_name, cms_db_user, cms_db_password, cms_root_password)
        # stop_service(cms_name)
        return redirect("/services")
    else:
        return redirect("/login")
    


@services_module.route("/start_service/<cms_name>",methods=["GET","POST"])
def start_services(cms_name):
    if request.method == "GET" and check_is_logged():
        start_service(cms_name)
        return redirect("/services")  
    else:
        return redirect("/login")


@services_module.route("/stop_service/<cms_name>", methods=["GET"])
def stop_services(cms_name):
    if request.method == "GET" and check_is_logged():
        stop_service(cms_name)
        return redirect("/services")
    else:
        return redirect("/login")


@services_module.route("/delete_service/<cms_name>", methods=["GET", "POST"])
def delete_services(cms_name):
    if request.method == "GET" and check_is_logged():
        delete_service(cms_name)
        return redirect("/services")
    else:
        return redirect("/login")