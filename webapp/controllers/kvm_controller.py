from flask import Blueprint, request, render_template, redirect, make_response
from controllers.login_controller import check_is_logged


kvm_module = Blueprint('kvm_module', __name__, template_folder='templates')


@kvm_module.route("/kvm")
def user_kvm():
    if request.method == "GET" and check_is_logged():
        return render_template("user_kvm.html")
    else:
        return "please log in"

@kvm_module.route("/kvm_create")
def user_kvm_create():
    if request.method == "GET" and check_is_logged():
        return render_template("user_kvm_create.html")
    else:
        return "please log in"