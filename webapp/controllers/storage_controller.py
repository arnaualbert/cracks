from flask import Blueprint, request, render_template, redirect,session, make_response,send_file, abort
from controllers.login_controller import check_is_logged
from py_access_system.storage_UpDown import crear_user_espacio, crear_carpeta, get_all_from_user
import os

storage_module = Blueprint('storage_module', __name__, template_folder='templates')


@storage_module.route("/storage")
def user_storage():
    username = session.get("username")
    crear_user_espacio()
    paths =get_all_from_user(username)
    if request.method == "GET" and check_is_logged():
        username = session.get("username")
        paths = get_all_from_user(username)
        return render_template("user_storage.html",paths=paths)
    else:
        return redirect("/login")


@storage_module.route('/download_file/<path:filename>')
def download_file(filename):
    try:
        base_dir = f"/home/arnau/users_storage/pepe"
        # Safely join the base directory and the requested file
        file_path = os.path.join(base_dir, filename)
        
        # Ensure the file exists
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            abort(404)  # File not found
    except Exception as e:
        abort(500)  # Internal server error


@storage_module.route('/delete_file/<path:filename>')
def delete_file(filename):
    try:
        base_dir = f"/home/arnau/users_storage/pepe"
        # Safely join the base directory and the requested file
        file_path = os.path.join(base_dir, filename)
        
        # Ensure the file exists
        if os.path.isfile(file_path):
            os.remove(file_path)
            return redirect("/storage")
        else:
            abort(404)  # File not found
    except Exception as e:
        abort(500)  # Internal server error



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