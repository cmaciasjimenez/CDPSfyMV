#!/usr/bin/python

# Script para instalar y ejecutar la pfinal2 de CDPS

print 'Practica final 2 de CDPS'
print 'Gonzalo Velasco Martin'
print 'Carlos Macias Jimenez'

import sys
import os
import time

print 'Empezando Script'

# Para comprobar cuanto tiempo tarda todo el script
start_time = time.time()

# Actualizamos
os.system("sudo apt-get update")
#Instalamos nano
os.system("sudo apt-get install nano")


# Comprobamos si ya existe el directorio y, si no, lo creamos
if os.path.exists("CDPS"):
        print('Directorio ya existe')
	os.chdir("CDPS")
elif not os.path.exists("CDPS"):
        os.system("mkdir CDPS")
        os.chdir("CDPS")

# Bajamos la ultima version de p7
os.system("wget http://idefix.dit.upm.es/download/cdps/p7/p7.tgz")
os.system("tar xfvz p7.tgz")
os.chdir("p7")

# Borramos p7.xml y bajamos el p7.xml que incluye Nagios
#os.system("rm -rf p7.xml")
#os.system("wget https://raw.githubusercontent.com/cmaciasjimenez/CDPSfyMV/master/p7.xml")


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

os.system("cd /etc/")
os.system("ls")
os.system("rm -r hosts")
os.system("wget https://raw.githubusercontent.com/cmaciasjimenez/CDPSfyMV/master/Host/hosts")


################################################################
## SERVIDORES WEB ## 
################################################################

# Montaje Servidores Web
os.system("lxc-attach -n s1 -- sudo apt-get install curl")
os.system("lxc-attach -n s2 -- sudo apt-get install curl")
os.system("lxc-attach -n s3 -- sudo apt-get install curl")
os.system("lxc-attach -n s4 -- sudo apt-get install curl")

os.system("lxc-attach -n s1 -- sudo curl --silent --location https://deb.nodesource.com/setup_4.x | sudo bash -")
os.system("lxc-attach -n s2 -- sudo curl --silent --location https://deb.nodesource.com/setup_4.x | sudo bash -")
os.system("lxc-attach -n s3 -- sudo curl --silent --location https://deb.nodesource.com/setup_4.x | sudo bash -")
os.system("lxc-attach -n s4 -- sudo curl --silent --location https://deb.nodesource.com/setup_4.x | sudo bash -")

os.system("lxc-attach -n s2 -- git clone https://github.com/cmaciasjimenez/CDPSfyTracks.git")
os.system("lxc-attach -n s3 -- git clone https://github.com/cmaciasjimenez/CDPSfyTracks.git")
os.system("lxc-attach -n s4 -- git clone https://github.com/cmaciasjimenez/CDPSfyTracks.git")

os.system("lxc-attach -n s2 -- cd CDPSfyTracks/tracks")
os.system("lxc-attach -n s3 -- cd CDPSfyTracks/tracks")
os.system("lxc-attach -n s4 -- cd CDPSfyTracks/tracks")

os.system("lxc-attach -n s2 -- mkdir /mnt/nas")
os.system("lxc-attach -n s3 -- mkdir /mnt/nas")
os.system("lxc-attach -n s4 -- mkdir /mnt/nas")

os.system("lxc-attach -n s2 -- mount -t glusterfs 10.1.3.21:/nas /mnt/nas")
os.system("lxc-attach -n s3 -- mount -t glusterfs 10.1.3.21:/nas /mnt/nas")
os.system("lxc-attach -n s4 -- mount -t glusterfs 10.1.3.21:/nas /mnt/nas")

os.system("lxc-attach -n s2 -- cd ..")
os.system("lxc-attach -n s3 -- cd ..")
os.system("lxc-attach -n s4 -- cd ..")

os.system("lxc-attach -n s1 -- cd /etc")
os.system("lxc-attach -n s1 -- sudo rm -r hosts")
os.system("wget https://raw.githubusercontent.com/cmaciasjimenez/CDPSfyMV/master/Host/S1/hosts")
os.system("lxc-attach -n s1 -- git clone https://github.com/cmaciasjimenez/CDPSfyServer.git")
os.system("lxc-attach -n s1 -- cd CDPSfyServer")
os.system("lxc-attach -n s1 -- npm install")

print('Servidores montados con exito')

################################################################
## INICIAMOS SERVIDORES ## 
################################################################

os.system("lxc-attach -n s1 -- npm start")
os.system("lxc-attach -n s2 -- npm start")
os.system("lxc-attach -n s3 -- npm start")
os.system("lxc-attach -n s4 -- npm start")

################################################################
## NAGIOS ## 
################################################################

# Instalamos lo necesario para Nagios
os.system("lxc-attach -n nagios -- apt-get update")
os.system("lxc-attach -n nagios -- apt-get install nano")
os.system("lxc-attach -n nagios -- apt-get install apache2 -y")
os.system("lxc-attach -n nagios -- apt-get install nagios3 -y")
os.system("lxc-attach -n nagios -- service apache2 restart")

# Bajamos los config files para los servidores
os.system("lxc-attach -n nagios -- wget https://raw.githubusercontent.com/cmaciasjimenez/CDPSfyMV/master/Nagios/s1_nagios2.cfg -P /etc/nagios3/conf.d")
os.system("lxc-attach -n nagios -- wget https://raw.githubusercontent.com/cmaciasjimenez/CDPSfyMV/master/Nagios/s2_nagios2.cfg -P /etc/nagios3/conf.d")
os.system("lxc-attach -n nagios -- wget https://raw.githubusercontent.com/cmaciasjimenez/CDPSfyMV/master/Nagios/s3_nagios2.cfg -P /etc/nagios3/conf.d")
os.system("lxc-attach -n nagios -- wget https://raw.githubusercontent.com/cmaciasjimenez/CDPSfyMV/master/Nagios/s4_nagios2.cfg -P /etc/nagios3/conf.d")

# Cambiamos el hostgroups por el de nuestro GitHub
os.system("lxc-attach -n nagios -- rm -rf /etc/nagios3/conf.d/hostgroups_nagios2.cfg")
os.system("lxc-attach -n nagios -- wget https://raw.githubusercontent.com/cmaciasjimenez/CDPSfyMV/master/Nagios/hostgroups_nagios2.cfg -P /etc/nagios3/conf.d/hosts.cfg")

# Reiniciamos nagios3 y apache2
os.system("lxc-attach -n nagios -- apt-get install apache2 -y")
os.system("lxc-attach -n nagios -- apt-get install nagios3 -y")

################################################################
## BALANCEADOR LB ## 
################################################################

os.system("xterm -hold -e 'lxc-attach -n lb -- xr --verbose --server tcp:0:80 --backend 10.1.2.12:3000 --backend 10.1.2.13:3000 --backend 10.1.2.14:3000 --web-interface 0:8001 -dr'")

# Imprimimos el tiempo que ha tardado en ejecutarse el script total:
print("seconds: " % (time.time() - start_time))

print('Fin del script')
