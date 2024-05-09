from flask import Flask, render_template, request, redirect
from controllers.login_controller import check_is_logged
from controllers.login_controller import login_module
from controllers.databases_controller import databases_module
from controllers.kvm_controller import kvm_module
from controllers.services_controller import services_module
from controllers.storage_controller import storage_module
from controllers.userAccount_controller import user_module
from controllers.contactUs_controller import contact_module

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.register_blueprint(login_module)
app.register_blueprint(databases_module)
app.register_blueprint(kvm_module)
app.register_blueprint(services_module)
app.register_blueprint(storage_module)
app.register_blueprint(user_module)
app.register_blueprint(contact_module)

@app.route("/",methods=["GET","POST"])
def home_page():
    if request.method == "GET":
        return render_template("index.html")


@app.route("/home_user")
def home_user():
    if request.method == "GET" and check_is_logged():
        return render_template("home_user.html")
    else:
        return redirect("/login")
