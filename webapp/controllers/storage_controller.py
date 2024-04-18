from flask import Blueprint, request, render_template, redirect, make_response
from controllers.login_controller import check_is_logged


storage_module = Blueprint('storage_module', __name__, template_folder='templates')


@storage_module.route("/storage")
def user_storage():
    if request.method == "GET" and check_is_logged():
        return render_template("user_storage.html")
    else:
        return redirect("/login")

@storage_module.route("/storage_create")
def user_storage_create():
    if request.method == "GET" and check_is_logged():
        return render_template("user_storage_create.html")
    else:
        return redirect("/login")