import subprocess
from controllers.login_controller import get_connection
from flask import Flask, render_template, request, redirect, session
import os
import own_env
def create_vm(kvm_name,kvm_memory,kvm_cpus):


    command = f"""tsp virt-install --name {kvm_name} --memory {kvm_memory} --vcpus {kvm_cpus} --disk size=15 --cdrom /var/lib/libvirt/images/bionicpup64-8.0-uefi.iso --import --network network:hostbridge --vnc --os-variant unknown"""
    kvm_iso = "bionicpup64-8.0-uefi.iso"
    try:
        subprocess.call(command,shell=True)
        print(f"VM {kvm_name} created successfully.")
        username = session.get("username")
        # Insertar datos en la tabla user_kvm
        insert_kvm(kvm_name, kvm_memory, kvm_cpus, kvm_iso, username)
        # os.chmod(f"/var/lib/libvirt/images/pepe5.qcow2",777)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def insert_kvm(kvm_name, kvm_memory, kvm_cpus, kvm_iso, username):
    conn = get_connection()
    cur = conn.cursor()
    print("asdsds")
    cur.execute("INSERT INTO user_kvm (kvm_name, kvm_memory, kvm_cpus, kvm_iso, username) VALUES (?, ?, ?, ?, ?)",(kvm_name, kvm_memory, kvm_cpus, kvm_iso, username))
    conn.commit()
    conn.close()
