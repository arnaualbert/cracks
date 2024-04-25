import subprocess
import re

def get_br0_ip():
    ip_add = subprocess.check_output(["ifconfig","br0"])
    ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', ip_add.decode())
    mask_match = re.search(r'mask (\d+\.\d+\.\d+\.\d+)', ip_add.decode())
    if ip_match and mask_match:
        ip = ip_match.group(1)
        mask = mask_match.group(1)
        mask_calc = sum(bin(int(x)).count('1') for x in mask.split('.'))
        return f"{ip}/{mask_calc}"
    else:
        return None

def get_xml(vm_name):
    output_xml = subprocess.check_output(["virsh", f"dumpxml --domain {vm_name}"])
    return output_xml.decode()

def get_mac(vm_name):
    xml_parse = get_xml(vm_name)

    print(xml_parse)

print(get_mac("1610master"))

def do_nmap_analysis():
    pass

def get_ip():
    pass