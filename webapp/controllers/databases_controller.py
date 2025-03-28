from flask import Blueprint, request, render_template, redirect,session, make_response
from controllers.login_controller import check_is_logged
from py_access_system.database_create import create_database, get_databases, database_delete

databases_module = Blueprint('databases_module', __name__, template_folder='templates')



@databases_module.route("/database")
def user_databases():
    username = session.get("username")
    if request.method == "GET" and check_is_logged():
        get_db = get_databases(username)
        return render_template("user_databases.html", username=username, databases=get_db)
    else:
        return "please log in"

@databases_module.route("/database_create")
def user_database_create():
    username = session.get("username")
    if request.method == "GET" and check_is_logged():
        return render_template("user_database_create.html", username=username)
    else:
        return redirect("/login")
    

@databases_module.route("/create_database", methods=["GET","POST"])
def user_create_database():
    if request.method == "POST" and check_is_logged():
        database_type = request.form["dbType"]
        database_name = request.form["dbName"]
        database_user = request.form["dbAdminUser"]
        database_password = request.form["dbAdminPassword"]
        current_user = session.get("username")
        create_database(database_type,database_password,database_name,database_user,current_user)
        return redirect("/database")
    else:
        return redirect("/login")


@databases_module.route("/delete_database/<database_name>",methods=["GET","POST"])
def delete_db_docker(database_name):
    if request.method == "GET" and check_is_logged():
        database_delete(database_name)
        return redirect("/database")
    else:
        return redirect("/login")