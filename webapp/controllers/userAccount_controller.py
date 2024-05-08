from flask import Blueprint, request, render_template, redirect, make_response, session, jsonify
from controllers.login_controller import check_is_logged
from py_access_system.kvm_create import create_vm, create_config_vm
from py_access_system.kvm_delete import delete_vm
from controllers.login_controller import get_connection
from py_access_system.kvm_start import start_vm, stop_vm, get_all_vm
from py_access_system.kvm_get_ip_by_vm_name import get_ip_kvm
import hashlib

user_module = Blueprint('user_module', __name__, template_folder='templates')


@user_module.route("/user_account")
def user_accountt():
    username = session.get("username")
    if request.method == "GET" and check_is_logged():
        info_user=select_user()
        return render_template("user_Account.html", info_user=info_user, username=username)
    else:
        return redirect("/login")
    
@user_module.route("/user_update_datos",  methods=["POST"])
def user_update():
    if request.method == "POST" and check_is_logged():
        user_name = request.form["username"]
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        password = request.form["password"]
        password_db = hashlib.sha256(password.encode("utf-8")).hexdigest()
        update_from_db(user_name,name,surname,email,password_db)
        return redirect("/login")
    
def update_from_db(username, name, surname, email, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Actualizamos los datos del usuario en la base de datos
        cur.execute("UPDATE users SET name = ?, surname = ?, email = ?, password = ? WHERE username = ?",
                    (name, surname, email, password, username))
        conn.commit()
        print("Datos de usuario actualizados correctamente")
    except Exception as e:
        print(f"Ocurrió un error al actualizar los datos del usuario: {e}")
    finally:
        conn.close()
    
def select_user():
    info_user=[]
    username = session.get("username")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?",(username,))
    rows = cursor.fetchall()
    if rows:
        for valor in rows:
            user_name=valor[0]
            name=valor[1]
            surname=valor[2]
            email=valor[3]
            password=valor[4]
            info_user.append({"user_name":user_name,"name":name,"surname":surname,"email":email, "password":password})

        conn.close()
        return info_user
    else:
        conn.close()
        return info_user