import subprocess
from controllers.login_controller import get_connection
from flask import Flask, render_template, request, redirect, session
import os
import own_env



def create_config_vm(hostname, password):
    config_word_list = ["#cloud-config",f"password: {password}", "chpasswd: { expire: False }", "ssh_pwauth: True", f"hostname: {hostname}"]
    file_path = "/home/arnau/Desktop/config-1.txt"    

    if not os.path.exists(file_path):
        # If the file doesn't exist, create it
        open(file_path, 'w').close()


    with open(file_path, "w") as file:
        for word in config_word_list:
            file.write(word + "\n")

    passw = own_env.getenv("PASSWORD_ROOT")
    command = f"""echo '{passw}' | sudo -S cloud-localds /var/lib/libvirt/{hostname}.img {file_path}"""
    subprocess.call(command,shell=True)
    return f"/var/lib/libvirt/{hostname}.img"

def create_vm(kvm_name,kvm_memory,kvm_cpus,iso,img_disk_info):
    passw = own_env.getenv("PASSWORD_ROOT")
    dict_iso_img = {"jammy":"jammy-server-cloudimg-amd64-disk-kvm.img","xenial":"xenial-server-cloudimg-amd64-disk1.img","mantic":"mantic-server-cloudimg-amd64.img","focal":"focal-server-cloudimg-amd64.img"}
    command_1 = f"""echo '{passw}' | sudo -S qemu-img convert -f qcow2 /var/lib/libvirt/images/{dict_iso_img[iso]} /var/lib/libvirt/images/{kvm_name}.img"""
    command_2 = f"""echo '{passw}' | sudo -S  virt-install  --name {kvm_name}  --memory {kvm_memory} --disk /var/lib/libvirt/images/{kvm_name}.img,device=disk,bus=virtio  --disk {img_disk_info},device=cdrom --os-variant ubuntu16.04  --virt-type kvm  --graphics none  --network network=hostbridge,model=virtio  --import"""
    command_list = [command_1, command_2]
    try:
        for command in command_list:
            subprocess.call(command,shell=True)
        print(f"VM {kvm_name} created successfully.")
        username = session.get("username")
        insert_kvm(kvm_name, kvm_memory, kvm_cpus, iso, username)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def insert_kvm(kvm_name: str, kvm_memory: int, kvm_cpus: int, kvm_iso: str, username: str):
    """
    Inserta información de una máquina virtual en la base de datos.

    Args:
        kvm_name (str): Nombre de la máquina virtual.
        kvm_memory (int): Cantidad de memoria asignada a la máquina virtual (en MB).
        kvm_cpus (int): Número de CPUs asignadas a la máquina virtual.
        kvm_iso (str): Ruta del archivo ISO utilizado para instalar el sistema operativo en la máquina virtual.
        username (str): Nombre de usuario asociado a la máquina virtual.

    Returns:
        None
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO user_kvm (kvm_name, kvm_memory, kvm_cpus, kvm_iso, username) VALUES (?, ?, ?, ?, ?)",
                (kvm_name, kvm_memory, kvm_cpus, kvm_iso, username))
    conn.commit()
    conn.close()

