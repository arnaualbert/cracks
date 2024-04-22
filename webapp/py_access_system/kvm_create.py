import subprocess
from controllers.login_controller import get_connection
from flask import Flask, render_template, request, redirect, session

def create_vm(vm_name,ram,cpus):
    

    command = f"""tsp virt-install --name {vm_name} --memory {ram} --vcpus {cpus} --disk size=15 --cdrom /var/lib/libvirt/images/bionicpup64-8.0-uefi.iso --import --network network:hostbridge --vnc --os-variant unknown"""

    try:
        subprocess.call(command,shell=True)
        print(f"VM {vm_name} created successfully.")
        username = session.get("username")
        # Insertar datos en la tabla user_kvm
        insert_kvm(username,vm_name)
        print("ASsadsad")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def insert_kvm(username,vm_name):
    conn = get_connection()
    cur = conn.cursor()
    print("asdsds")
    cur.execute("INSERT INTO user_kvm (kvm_name, username) VALUES (?, ?)",(vm_name,username))
    conn.commit()
    conn.close()
