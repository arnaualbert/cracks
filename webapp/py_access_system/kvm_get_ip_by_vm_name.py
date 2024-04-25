import subprocess
import re
import xml.etree.ElementTree as ET

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
    et_parser = ET.fromstring(xml_parse)
    interface = et_parser.find(".//interface")
    mac_address = interface.find("mac").attrib["address"]
    return mac_address

def do_nmap_analysis():
    ip_to_parse = get_br0_ip()
    subprocess.run(["nmap","-sP",ip_to_parse],stdout = subprocess.DEVNULL)

def get_ip_kvm(vm_name):
    do_nmap_analysis()
    mac_add = get_mac(vm_name)
    out_arp = subprocess.check_output(["arp","-a"])
    dec = out_arp.decode()
    list_of_parsed_ip = dec.split("\n")
    for ip_info in list_of_parsed_ip:
        if mac_add in ip_info:
            ip_pattern = r'\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)'
            match = re.search(ip_pattern, ip_info)
            if match:
                return match.group(1)
            else:
                return None

print(get_ip_kvm("1605master"))