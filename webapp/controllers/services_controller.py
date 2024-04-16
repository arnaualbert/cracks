from flask import Blueprint, request, render_template, redirect, make_response
from controllers.login_controller import check_is_logged


services_module = Blueprint('services_module', __name__, template_folder='templates')



@services_module.route("/services")
def user_services():
    if request.method == "GET" and check_is_logged():
        return render_template("user_services.html")
    else:
        return "please log in"

@services_module.route("/service_create")
def user_service_create():
    if request.method == "GET" and check_is_logged():
        return render_template("user_service_create.html")
    else:
        return "please log in"