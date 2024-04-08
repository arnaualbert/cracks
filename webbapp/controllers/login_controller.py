from flask import Blueprint, request, render_template, redirect, make_response
import mariadb
import os
import hashlib


login_module = Blueprint('login_module', __name__, template_folder='templates')

def check_is_logged():
    if request.cookies.get("username") is not None:
        return True
    else:
        return False


def get_connection():
    conn = mariadb.connect(
        user = os.getenv("USERDB"),
        password= os.getenv("PASSWORD"),
        host="localhost",
        port=3306,
        database=os.getenv("DATABASE")
    )
    return conn


def log_user(username: str,password: str) -> bool:
    """
    Verifica las credenciales de inicio de sesión de un usuario.

    Args:
        username (str): Nombre de usuario del usuario.
        password (str): Contraseña del usuario.

    Returns:
        bool: True si las credenciales son válidas y el usuario existe en la base de datos, False de lo contrario.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",(username,password))
    rows = cursor.fetchall()
    if rows:
        conn.close()
        return True
    else:
        conn.close()
        return False

def username_exist(username: str) -> bool:
    """
    Verifica si un nombre de usuario ya existe en la base de datos.

    Args:
        username (str): Nombre de usuario a verificar.

    Returns:
        bool: True si el nombre de usuario ya existe en la base de datos, False de lo contrario.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?",(username,))
    rows = cursor.fetchall()
    if rows:
        conn.close()
        return True
    else:
        conn.close()
        return False


def register_user(username: str,name: str,surname: str,email: str,password: str) -> bool:
    """
    Registra un nuevo usuario en la base de datos.

    Args:
        username (str): Nombre de usuario único.
        name (str): Nombre del usuario.
        surname (str): Apellido del usuario.
        email (str): Correo electrónico del usuario.
        password (str): Contraseña del usuario.

    Returns:
        bool: True si el usuario se registró correctamente, False si el nombre de usuario ya existe.
    """
    conn = get_connection()
    exist_account = username_exist(username)
    if exist_account:
        return False
    elif not exist_account:
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username,name,surname,email,password) VALUES (?,?,?,?,?)",(username,name,surname,email,password))
        conn.commit()
        conn.close()
        return True


@login_module.route("/login", methods=["GET","POST"])
def login():
    """
    Maneja la página de inicio de sesión.

    Método GET:
        Devuelve la página de inicio de sesión.

    Método POST:
        Recoge los datos del formulario de inicio de sesión y procesa la solicitud.
        Verifica las credenciales del usuario llamando a la función log_user().
        Si las credenciales son válidas, redirige al usuario a la página de inicio de sesión.
        Si las credenciales son inválidas, redirige al usuario a la página de inicio de sesión.

    Returns:
        render_template o redirect: Devuelve una plantilla HTML si las credenciales son inválidas, o redirige al usuario a otra página si las credenciales son válidas.
    """
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_db = hashlib.sha256(password.encode('utf-8')).hexdigest() 
        user_exist = log_user(username,password_db)
        if user_exist:
            resp = make_response(redirect("/home_user"))
            resp.set_cookie("username",username)
            return resp
        else:
            return redirect("/login")


@login_module.route("/register", methods=["GET","POST"])
def register():
    """
    Maneja el registro de nuevos usuarios.

    Método GET:
        Devuelve la página de registro.

    Método POST:
        Recoge los datos del formulario de registro y procesa la solicitud.
        Si la contraseña y la confirmación de contraseña coinciden, intenta registrar al usuario.
        Si el registro tiene éxito, muestra un mensaje de éxito.
        Si el nombre de usuario ya existe, muestra un mensaje de error.
        Si las contraseñas no coinciden, muestra un mensaje de error.

    Returns:
        render_template: Devuelve una plantilla HTML con mensajes según el resultado del registro.
    """
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        username =  request.form["username"]
        password = request.form["password"]
        password_confirm = request.form["passwordrepeat"]
        if password == password_confirm:
            password_db = hashlib.sha256(password.encode("utf-8")).hexdigest()
            registered = register_user(username,name,surname,email,password_db)
            if registered:
                return render_template("register.html",message="Registered successfully.")
            else:
                return render_template("register.html",message="Username already exist, try again.")
        else:
            return render_template("register.html",message="The passwords doesn't match, try again.")


@login_module.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.delete_cookie("username")
    return resp