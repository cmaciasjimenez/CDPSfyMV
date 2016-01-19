#!/usr/bin/python

print 'Practica final 2 de CDPS'
print 'Gonzalo Velasco Martin'
print 'Carlos Macias Jimenez'

import sys
import os


print 'Empezando Script'

# Actualizamos
os.system("sudo apt-get update")
#Instalamos nano
os.system("sudo apt-get install nano")


# Comprobamos si ya existe el directorio y, si no, lo creamos
if os.path.exists("CDPS")):
        print('Directorio ya existe')
elif not os.path.exists("CDPS")
        os.system("mkdir CDPS")
        os.chdir("CDPS")

# Bajamos la ultima version de p7
os.system("wget http://idefix.dit.upm.es/download/cdps/p7/p7.tgz")
os.system("tar xfvz p7.tgz")
os.chdir("p7")

# Arrancamos el escenario
os.system("./bin/prepare-p7-vm")
os.system("vnx -f p7.xml -v --create")



