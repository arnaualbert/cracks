from flask import Blueprint, request, render_template, redirect, make_response
from controllers.login_controller import check_is_logged

databases_module = Blueprint('databases_module', __name__, template_folder='templates')



@databases_module.route("/database")
def user_databases():
    if request.method == "GET" and check_is_logged():
        return render_template("user_databases.html")
    else:
        return "please log in"