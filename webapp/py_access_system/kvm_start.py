import subprocess

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