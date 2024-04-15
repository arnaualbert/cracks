#!/bin/bash

#avisamos al usuario que se ejecuta el script con un suario con prevelgios (tiene que hacer instlaciones necesita preveljios)
if [ $(id -u) -eq "0" ]; then
echo "el script ha ejecutado con el usario $(id -un) que tiene la UID igual a $(id -u). "
echo "!!!!!User With priviledge¡¡¡¡¡"
else
echo "el script ha ejecutado con el usario $(id -un) que tiene la UID igual a $(id -u). "
echo "!!!!!the script need User with previleges¡¡¡¡¡"
exit 1
fi
echo -e "\n"
echo "The setup of the service is started."
echo "preparando el entorno..."
echo -e "\n"

echo "Actualizando la sistema [update]..."
apt-get update > /dev/null
echo -e "\t\t ¡update Done!"
echo -e "\n"

#verificamos si las paquetes del servecio libvert estan Instaladas, sino las instalamos 
if ( ! dpkg -l | grep -qE "qemu-kv|qemu-system-x86|qemu" ) ; then
  echo "El paquete qemu-kvm no está instalada."
  echo "qemu-kvm: Herramienta de virtualización que permite ejecutar sistemas operativos y aplicaciones en entornos virtualizados."
  echo "Instalando."
  echo "Instalando.."
  echo "Instalando..."
  apt-get install qemu-kvm >/dev/null
  echo "Paquete qemu-kvm instalada correctamente."
  echo -e "\n"
fi
if ( ! dpkg -l | grep -q "libvirt-daemon-system" ) ; then
  echo "El paquete libvirt-daemon-system no está instalada."
  echo "libvirt-daemon-system: Demonio del sistema que gestiona la virtualización y proporciona una interfaz para interactuar con los recursos virtuales del sistema."
  echo "Instalando."
  echo "Instalando.."
  echo "Instalando..."
  apt-get -y install libvirt-daemon-system >/dev/null
  echo "Paquete libvirt instalada correctamente."
  echo -e "\n"
fi

if ( ! dpkg -l | grep -q "libvirt-clients" ) ; then
  echo "El paquete libvirt-client no está instalada."
  echo "libvirt-clients: Conjunto de herramientas de línea de comandos para interactuar con el demonio de libvirt y administrar máquinas virtuales."
  echo "Instalando."
  echo "Instalando.."
  echo "Instalando..."
  apt-get install -y libvirt-clients >/dev/null
  echo "Paquete libvirt-clientes instalada correctamente."
  echo -e "\n"
fi

if ( ! dpkg -l | grep -q "virt-manager" ) ; then
  echo "El paquete virt-manager no está instalada."
  echo "virt-manager: Interfaz gráfica para gestionar y crear máquinas virtuales utilizando libvirt."
  echo "Instalando."
  echo "Instalando.."
  echo "Instalando..."
  apt-get install -y virt-manager >/dev/null
  echo "Paquete virt-manager instalada correctamente."
  echo -e "\n"
fi

if ( ! dpkg -l | grep -q "bridge-utils" ) ; then
  echo "El paquete bridge-utils no está instalada."
  echo "bridge-utils: Conjunto de utilidades para configurar y administrar puentes de red en sistemas Linux."
  echo "Instalando."
  echo "Instalando.."
  echo "Instalando..."
  apt-get install -y bridge-utils >/dev/null
  echo "Paquete bridge-utils instalada correctamente."
  echo -e "\n"
fi


if ( ! dpkg -l | grep -q "virtinst" ) ; then
  echo "El paquete virtinst no está instalada."
  echo "virtinst: Conjunto de herramientas para la creación y gestión de máquinas virtuales basadas en libvirt, incluyendo la instalación automática de sistemas operativos invitados."
  echo "Instalando."
  echo "Instalando.."
  echo "Instalando..."
  apt-get install -y virtinst >/dev/null
  echo "Paquete virtinst instalada correctamente."
  echo -e "\n"
fi


if ( ! dpkg -l | grep -q "libguestfs-tools" ) ; then
  echo "El paquete libguestfs no está instalada."
  echo "Libguestfs: Una biblioteca para el acceso y modificación de imágenes de sistemas de archivos de máquinas virtuales."
  echo "Instalando."
  echo "Instalando.."
  echo "Instalando..."
  apt-get install -y libguestfs-tools >/dev/null
  echo "Paquete libguestfs instalada correctamente."
  echo -e "\n"
fi


if ( ! dpkg -l | grep -q "libosinfo-bin" ) ; then
  echo "El paquete libosinfo no está instalada."
  echo "libosinfo: Biblioteca para obtener información detallada sobre sistemas operativos y dispositivos en entornos de virtualización y gestión de sistemas."
  echo "Instalando."
  echo "Instalando.."
  echo "Instalando..."
  apt-get install -y libosinfo-bin >/dev/null
  echo "Paquete libosinfo instalada correctamente."
  echo -e "\n"
fi


echo "la muestra del servecio de virtualizacion LIBVIRT despues de haver instalado las paquetes necesarias"
echo "Iniciando el servecio libvirtd [start] & Asegura la presistencia del servecio libvirt [enable]"
systemctl start libvirtd
systemctl enable libvirtd
echo -e "\n"
echo "-------------Verifica el estado del servicio libvirtd [status]:-------------"
systemctl status libvirtd
echo "----------------------------------------------------------------------------"
echo -e "\n\n\n"
echo -e "\t\t The setup of the service is complete."
