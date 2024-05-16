from flask import Blueprint, request, render_template, redirect,session, make_response
from controllers.login_controller import check_is_logged
from py_access_system.storage_UpDown import crear_user_espacio, crear_carpeta

storage_module = Blueprint('storage_module', __name__, template_folder='templates')


@storage_module.route("/storage")
def user_storage():
    crear_user_espacio()
    if request.method == "GET" and check_is_logged():
        return render_template("user_storage.html")
    else:
        return redirect("/login")


    
#########################################
@storage_module.route("/new_folder", methods=["GET", "POST"])
def user_new_folder():
    username = session.get("username")
    if request.method == "GET" and check_is_logged():
        return render_template("user_storage.html", username=username)
    if request.method == "POST" and check_is_logged():

        folder_name = request.form.get("folderName")            
        crear_carpeta(folder_name, username)
     
        return redirect("/storage")
    else:
        return redirect("/login")
    

    
@storage_module.route("/upload_folder")
def user_upload_folder():
    if request.method == "GET" and check_is_logged():
        return render_template("user_storage_create.html")
    else:
        return redirect("/login")
    
@storage_module.route("/upload_file")
def user_upload_file():
    if request.method == "GET" and check_is_logged():
        return render_template("user_storage_create.html")
    else:
        return redirect("/login")