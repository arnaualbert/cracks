from flask import Blueprint, request, render_template, redirect, make_response, session
from controllers.login_controller import check_is_logged
from py_access_system.kvm_create import create_vm
from py_access_system.kvm_delete import delete_vm
from controllers.login_controller import get_connection

kvm_module = Blueprint('kvm_module', __name__, template_folder='templates')


@kvm_module.route("/kvm")
def user_kvm():
    if request.method == "GET" and check_is_logged():
        # return render_template("user_kvm.html")
        info_kvm=select_kvm()
        #info_kvm = [{"kvm_name":"test5","kvm_memory":"2048","kvm_cpu":"2","kvm_iso":"bionic"},{"kvm_name":"test5","kvm_memory":"2048","kvm_cpu":"2","kvm_iso":"bionic"},]
        return render_template("user_kvm.html",info=info_kvm)
    else:
        return redirect("/login")

def select_kvm():
    info_kvm=[]
    username = session.get("username")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_kvm WHERE username = ?",(username,))
    rows = cursor.fetchall()
    if rows:
        for valor in rows:
            kvm_name=valor[0]
            kvm_memory=valor[1]
            kvm_cpu=valor[2]
            kvm_iso=valor[3]
            info_kvm.append({"kvm_name":kvm_name,"kvm_memory":kvm_memory,"kvm_cpu":kvm_cpu,"kvm_iso":kvm_iso})

        conn.close()
        return info_kvm
    else:
        conn.close()
        return info_kvm


@kvm_module.route("/kvm_create", methods=["GET", "POST"])
def user_kvm_create():
    if request.method == "GET" and check_is_logged():
            return render_template("user_kvm_create.html")
    if request.method == "POST" and check_is_logged():
        vm_name = request.form.get("vmName")
        ram = request.form.get("ram")
        cpus = request.form.get("cpus")
        iso = request.form.get("iso")
        create_vm(vm_name,ram,cpus)
        username = session.get("username")
        # info = [{"kvm_name":"test5","kvm_memory":"2048","kvm_cpu":"2","kvm_iso":"bionic"},{"kvm_name":"test5","kvm_memory":"2048","kvm_cpu":"2","kvm_iso":"bionic"}]
        return render_template("user_kvm_create.html")
    else:
        return redirect("/login")
    
@kvm_module.route("/kvm_delete/<kvm_name>", methods=["GET", "POST"])
def user_kvm_delete(kvm_name):
    if request.method == "GET" and check_is_logged():
        delete_vm(kvm_name)
        return redirect("/kvm")
    else:
        return redirect("/login")