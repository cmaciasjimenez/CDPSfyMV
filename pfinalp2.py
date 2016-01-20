#!/usr/bin/python

print 'Practica final 2 de CDPS'
print 'Gonzalo Velasco Martin'
print 'Carlos Macias Jimenez'

import sys
import os
import time


print 'Empezando Script'

# Actualizamos
os.system("sudo apt-get update")
#Instalamos nano
os.system("sudo apt-get install nano")


# Comprobamos si ya existe el directorio y, si no, lo creamos
if os.path.exists("CDPS"):
        print('Directorio ya existe')
elif not os.path.exists("CDPS"):
        os.system("mkdir CDPS")
        os.chdir("CDPS")

# Bajamos la ultima version de p7
os.system("wget http://idefix.dit.upm.es/download/cdps/p7/p7.tgz")
os.system("tar xfvz p7.tgz")
os.chdir("p7")

# Arrancamos el escenario
os.system("./bin/prepare-p7-vm")
os.system("vnx -f p7.xml -v --destroy")
os.system("vnx -f p7.xml -v --create")

################################################################
## GLUSTER FS ## 
################################################################

# Montar Gluster FS
os.system("lxc-attach -n nas1 -- gluster peer probe 10.1.3.22")
os.system("lxc-attach -n nas1 -- gluster peer probe 10.1.3.23")

# Comprobamos que estan anadidos los peers
os.system("lxc-attach -n nas1 -- gluster peer status")

os.system("lxc-attach -n nas1 -- gluster volume create nas replica 3 10.1.3.21:/nas 10.1.3.22:/nas 10.1.3.23:/nas force")

# Arrancamos el volumen
os.system("lxc-attach -n nas1 -- gluster volume start nas")
time.sleep(10)

# Ver volumenes creados
os.system("lxc-attach -n nas1 -- gluster volume info")

################################################################
## SERVIDORES WEB ## 
################################################################

# Montaje Servidores Web
os.system("lxc-attach -n s1 -- sudo mkdir /mnt/nas")
os.system("lxc-attach -n s1 -- sudo mount -t glusterfs 10.1.3.21:/nas /mnt/nas")
os.system("lxc-attach -n s2 -- sudo mkdir /mnt/nas")
os.system("lxc-attach -n s2 -- sudo mount -t glusterfs 10.1.3.21:/nas /mnt/nas")
os.system("lxc-attach -n s3 -- sudo mkdir /mnt/nas")
os.system("lxc-attach -n s3 -- sudo mount -t glusterfs 10.1.3.21:/nas /mnt/nas")
os.system("lxc-attach -n s4 -- sudo mkdir /mnt/nas")
os.system("lxc-attach -n s4 -- sudo mount -t glusterfs 10.1.3.21:/nas /mnt/nas")

print('Servidores montados con exito')

# Configuracion del servidor
os.system("rm -rf /etc/hosts")
#os.system("wget https://raw.githubusercontent.com/cmaciasjimenez/CDPSfyMV/master/Host/hosts -P /etc")

# Instalamos en los servidores Node y el editor nano
#Descargamos e instalamos paquetes necesarios en S1, S2, S3 y S4
for n in range (1, 5):
	os.system("lxc-attach -n s" + str(n) + " -- apt-get update")
	os.system("lxc-attach -n s" + str(n) + " -- apt-get install software-properties-common -y")
	os.system("lxc-attach -n s" + str(n) + " -- apt-get install git -y")
	os.system("lxc-attach -n s" + str(n) + " -- apt-get install make g++ -y")
	os.system("lxc-attach -n s" + str(n) + " -- apt-get install python-software-properties -y")
	os.system("lxc-attach -n s" + str(n) + " -- add-apt-repository ppa:chris-lea/node.js -y")
	os.system("lxc-attach -n s" + str(n) + " -- apt-get update")
	os.system("lxc-attach -n s" + str(n) + " -- apt-get install nodejs -y")
	os.system("lxc-attach -n s" + str(n) + " -- apt-get install nano -y")

# Clonamos CDPSfyTracks en S2, S3 y S4
for n in range (2, 5):
	os.system("lxc-attach -n s" + str(n) + " -- git clone https://github.com/cmaciasjimenez/CDPSfyTracks.git")
	execute = "'cd /CDPSfyTracks/ && node app.js'"
	# Lo ejecutamos
	os.system('xterm -hold -e "lxc-attach -n s' + str(n) + ' -- sh -c ' + execute + '" &')

# Configuracion del servidor S1
os.system("lxc-attach -n s1 -- rm -rf /etc/hosts")
os.system("lxc-attach -n s1 -- wget https://raw.githubusercontent.com/cmaciasjimenez/CDPSfyMV/master/Host/S1/hosts -P /etc")

################################################################
## BALANCEADOR DE CARGA ## 
################################################################

# LB CrossRoads. LB en el puerto 80. Servicios activos en S2, S3 y S4 y Servidor web para gestion en el puerto 8001 del LB
os.system("xterm -hold -e 'lxc-attach -n lb -- xr --verbose --server tcp:0:80 --backend 10.1.2.12:3000 --backend 10.1.2.13:3000 --backend 10.1.2.14:3000 --web-interface 0:8001'")

print('Fin del script')