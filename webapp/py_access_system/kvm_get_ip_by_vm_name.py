import subprocess
import re
import xml.etree.ElementTree as ET

def get_br0_ip():# -> str|None:
    """
    Obtiene la dirección IP y la máscara de subred de la interfaz de red 'br0'.
    Calcula la máscara de subred en formato CIDR y devuelve la dirección IP en ese formato,
    o None si no se puede obtener la información.
    
    Returns:
        str|None: Dirección IP en formato CIDR o None si la información no está disponible.
    """
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

def get_xml(vm_name: str):# -> str:
    """
    Obtiene el XML que describe la configuración de la máquina virtual especificada.
    
    Args:
        vm_name (str): Nombre de la máquina virtual.
    
    Returns:
        str: XML que describe la configuración de la máquina virtual.
    """
    output_xml = subprocess.check_output(["virsh", f"dumpxml --domain {vm_name}"])
    return output_xml.decode()

def get_mac(vm_name: str):# -> str:
    """
    Obtiene la dirección MAC de la interfaz de red de la máquina virtual especificada.
    
    Args:
        vm_name (str): Nombre de la máquina virtual.
    
    Returns:
        str: Dirección MAC de la interfaz de red.
    """
    xml_parse = get_xml(vm_name)
    et_parser = ET.fromstring(xml_parse)
    interface = et_parser.find(".//interface")
    mac_address = interface.find("mac").attrib["address"]
    return mac_address

def do_nmap_analysis():
    """
    Realiza un escaneo de hosts en la red br0 utilizando el comando nmap con la opción -sP.
    La salida se redirige a /dev/null para que no se muestre en la consola.
    """
    ip_to_parse = get_br0_ip()
    subprocess.run(["nmap","-sP",ip_to_parse],stdout = subprocess.DEVNULL)

def get_ip_kvm(vm_name: str):# -> str|None:
    """
    Obtiene la dirección IP de la máquina virtual especificada en la red.
    
    Args:
        vm_name (str): Nombre de la máquina virtual.
    
    Returns:
        str|any|None: Dirección IP de la máquina virtual, None si no se puede obtener.
    """
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
