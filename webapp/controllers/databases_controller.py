from flask import Blueprint, request, render_template, redirect, make_response
from controllers.login_controller import check_is_logged
from py_access_system.database_create import create_database

databases_module = Blueprint('databases_module', __name__, template_folder='templates')



@databases_module.route("/database")
def user_databases():
    if request.method == "GET" and check_is_logged():
        return render_template("user_databases.html")
    else:
        return "please log in"

@databases_module.route("/database_create")
def user_database_create():
    if request.method == "GET" and check_is_logged():
        return render_template("user_database_create.html")
    else:
        return redirect("/login")
    

@databases_module.route("/create_database", methods=["GET","POST"])
def user_create_database():
    if request.method == "POST" and check_is_logged():
        database_type = request.form["dbType"]
        database_name = request.form["dbName"]
        database_user = request.form["dbAdminUser"]
        database_password = request.form["dbAdminPassword"]
        create_database(database_type,database_password,database_name,database_user)
        return redirect("/database")
    else:
        return redirect("/login")
