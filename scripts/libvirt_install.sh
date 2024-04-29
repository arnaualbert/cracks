#!/bin/bash

# Aseguramos de que el script se ejecute con privilegios de superusuario.
if [ "$(id -u)" -ne "0" ]; then
    echo "Este script necesita privilegios de superusuario para ejecutarse."
    exit 1
fi

# Notifica sobre el Inicio de las configuracion.
echo -e "\nEl proceso de configuración del servicio ha comenzado.\n"

# Actualizar el sistema.
echo "Actualizando el sistema..."
apt-get update > /dev/null
echo -e "\t\t ¡Actualización completa!\n"

# Definir una función para instalar paquetes si no están presentes.
install_package() {
    local package_name=$1
    local package_description=$2

    if ! dpkg -l | grep -qE "^ii\s+$package_name"; then
        echo "El paquete $package_name no está instalado."
        echo "$package_description"
        echo "Instalando..."
        apt-get install -y $package_name >/dev/null

        if [ $? -eq 0 ]; then
            echo "Paquete $package_name instalado correctamente."
        else
            echo "Error al instalar el paquete $package_name."
            exit 1
        fi
        echo -e "\n"
    fi
}

# Instalar paquetes necesarios
install_package "qemu-kvm" "qemu-kvm: Herramienta de virtualización que permite ejecutar sistemas operativos y aplicaciones en entornos virtualizados."
install_package "libvirt-daemon-system" "libvirt-daemon-system: Demonio del sistema que gestiona la virtualización y proporciona una interfaz para interactuar con los recursos virtuales del sistema."
install_package "libvirt-clients" "libvirt-clients: Conjunto de herramientas de línea de comandos para interactuar con el demonio de libvirt y administrar máquinas virtuales."
install_package "virt-manager" "virt-manager: Interfaz gráfica para gestionar y crear máquinas virtuales utilizando libvirt."
install_package "bridge-utils" "bridge-utils: Conjunto de utilidades para configurar y administrar puentes de red en sistemas Linux."
install_package "virtinst" "virtinst: Conjunto de herramientas para la creación y gestión de máquinas virtuales basadas en libvirt, incluyendo la instalación automática de sistemas operativos invitados."
install_package "libguestfs-tools" "Libguestfs: Una biblioteca para el acceso y modificación de imágenes de sistemas de archivos de máquinas virtuales."
install_package "libosinfo-bin" "libosinfo: Biblioteca para obtener información detallada sobre sistemas operativos y dispositivos en entornos de virtualización y gestión de sistemas."

# Verificar el estado del servicio libvirtd y activarlo.
echo "Iniciando el servicio libvirtd y asegurando su persistencia..."
systemctl start libvirtd
systemctl enable libvirtd
echo -e "\n"
echo "-------------Estado del servicio libvirtd:-------------"
echo "$(systemctl status libvirtd)"
echo "-------------------------------------------------------"
echo -e "\n\n\n"
echo -e "\t\t ¡La configuración del servicio está completa!"
