from flask import Blueprint, request, render_template, redirect, make_response
from controllers.login_controller import check_is_logged
from py_access_system.kvm_create import create_vm

kvm_module = Blueprint('kvm_module', __name__, template_folder='templates')


@kvm_module.route("/kvm")
def user_kvm():
    if request.method == "GET" and check_is_logged():
        return render_template("user_kvm.html")
    else:
        return redirect("/login")

@kvm_module.route("/kvm_create", methods=["GET", "POST"])
def user_kvm_create():
    if request.method == "GET" and check_is_logged():
            return render_template("user_kvm_create.html")
    if request.method == "POST" and check_is_logged():
        vm_name = request.form.get("vmName")
        ram = request.form.get("ram")
        cpus = request.form.get("cpus")
        iso = request.form.get("iso")
        create_vm(vm_name,ram,cpus,iso)

        
        return render_template("user_kvm_create.html")
    else:
        return redirect("/login")