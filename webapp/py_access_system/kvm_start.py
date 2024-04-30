import subprocess
from controllers.login_controller import get_connection

def get_all_vm():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT kvm_name FROM user_kvm")
    rows = cursor.fetchall()
    if rows:
        conn.close()
        return rows
    else:
        conn.close()
        return []


def start_vm(kvm_name):
    try:
        command_start = f"""virsh start {kvm_name}""" 
        subprocess.call(command_start, shell=True)
        print(f"VM {kvm_name} Started successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def stop_vm(kvm_name):
    try:
        command_start = f"""virsh shutdown {kvm_name}""" 
        subprocess.call(command_start, shell=True)
        print(f"VM {kvm_name} shutdown successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")