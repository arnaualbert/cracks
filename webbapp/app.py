from flask import Flask, render_template, request, redirect
from controllers.login_controller import check_is_logged
from controllers.login_controller import login_module

app = Flask(__name__)

app.register_blueprint(login_module)


@app.route("/",methods=["GET","POST"])
def home_page():
    if request.method == "GET":
        return render_template("index.html")


@app.route("/home_user")
def home_user():
    if request.method == "GET" and check_is_logged():
        return render_template("home_user.html")
    else:
        return "please log in"


@app.route("/logout")
def logout():
    if request.method == "GET":
        return redirect("/")
    