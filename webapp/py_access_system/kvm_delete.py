import subprocess
from controllers.login_controller import get_connection
from flask import Flask, render_template, request, redirect, session
import own_env

def delete_vm(kvm_name):
    try:
        passw = own_env.getenv("PASSWORD_ROOT")
        command_perms = f"echo '{passw}' | sudo -S chmod 777 /var/lib/libvirt/images/{kvm_name}*"
        command_destroy = f"""virsh destroy {kvm_name}"""
        command_undfine = f"""virsh undefine {kvm_name}"""
        command_rm = f"""rm /var/lib/libvirt/images/{kvm_name}.qcow2"""
        lis_cmd=[command_perms,command_destroy,command_undfine,command_rm]
        for cmd in lis_cmd:
            subprocess.call(cmd, shell=True)

        print(f"VM {kvm_name} deleted successfully.")

        # Eliminamos los datos de la vm en la base de datos la tabla user_kvm 
        delete_from_db(kvm_name)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def delete_from_db(kvm_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM user_kvm WHERE kvm_name=?", (kvm_name,))
    conn.commit()
    conn.close()
