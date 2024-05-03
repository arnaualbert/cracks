from flask import Blueprint, request, render_template, redirect, make_response
from controllers.login_controller import check_is_logged
from py_access_system.service_create import create_docker_compose
from py_access_system.service_create import create_service


services_module = Blueprint('services_module', __name__, template_folder='templates')



@services_module.route("/services")
def user_services():
    if request.method == "GET" and check_is_logged():
        return render_template("user_services.html")
    else:
        return redirect("/login")

@services_module.route("/service_create")
def user_service_create():

    if request.method == "POST" and check_is_logged():
        cms_type = request.form.get("cmsType")
        cms_name = request.form.get("cmsNmae")
        cms_db_user= request.form.get("cmsdbUser")
        cms_db_password= request.form.get("cmsdbPassword")
        cms_root_password = request.form.get("cmsrootPassword")
        forme_docker_compose = create_docker_compose(cms_type, cms_name, cms_db_user, cms_db_password, cms_root_password)
        create_service(forme_docker_compose)
        #stop_service(service)
        return redirect("/services")
    else:
        return redirect("/login")