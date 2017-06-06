#!/bin/bash

if [ "`whoami`" != "root" ]; then
	echo "Has de ser root o ejecutarlo como root para poder seguir"
	exit
fi

DIRNAME="$(dirname $0)"
INSTALLATION_DIR="/opt"
INSTALLATION_PROJECT="$INSTALLATION_DIR/OSCP"
EXECUTABLE_DIR="$INSTALLATION_PROJECT/notas.py"

RESTORE='\033[0m'
RED='\033[00;31m'
GREEN='\033[00;32m'
LBLUE='\033[01;34m'

clear

echo -e "$GREEN░▀█▀░█▀█░█▀▀░▀█▀░█▀█░█░░░█▀█░█▀▀░▀█▀░█▀█░█▀█░░░█▀█░█▀▀░█▀▀░█▀█$RESTORE"
echo -e "$GREEN░░█░░█░█░▀▀█░░█░░█▀█░█░░░█▀█░█░░░░█░░█░█░█░█░░░█░█░▀▀█░█░░░█▀▀$RESTORE"
echo -e "$GREEN░▀▀▀░▀░▀░▀▀▀░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░░▀▀▀░▀▀▀░▀▀▀░▀░░$RESTORE"

echo -e "\n$GREEN[+]$RESTORE Instalando aplicacion en" $INSTALLATION_DIR 

# Comprueba que estan instaladas las dependencias de python necesarias
echo -e "$GREEN[+]$RESTORE Comprobando dependencias de python"
python -c "import termcolor" 2> /dev/null
if [ $? -ne 0 ]; then
	echo -e "$LBLUE[!]$RESTORE Instalando libreria termcolor"
fi
python -c "import git" 2> /dev/null
if [ $? -ne 0 ]; then
	echo -e "$LBLUE[!]$RESTORE Instalando libreria git"
fi
python -c "import shutil" 2> /dev/null
if [ $? -ne 0 ]; then
	echo -e "$LBLUE[!]$RESTORE Instalando libreria shutil"
fi
echo -e "$GREEN[+]$RESTORE Librerias de python comprobadas e instaladas"

# Comprueba si existe el directorio de instalacion
if [ ! -d $INSTALLATION_PROJECT ]; then
	mkdir $INSTALLATION_PROJECT 
	echo -e "$GREEN[+]$RESTORE Directorio" $INSTALLATION_PROJECT" creado correctamente"
	
	# Copia ficheros y directorios al directorio de instalacion	
	find . -maxdepth 1 -type f  -exec cp {} $INSTALLATION_PROJECT \;
	find . -maxdepth 1 -type d  -not -path '*/\.*' -exec cp -r {} $INSTALLATION_PROJECT \;

	echo -e "$GREEN[+]$RESTORE Ficheros copiados a $INSTALLATION_PROJECT correctamente"
else
	echo -e "$RED[-]$RESTORE El directorio $INSTALLATION_PROJECT ya existe\n"
	exit
fi

# Crea un alias para ejecutarlo desde cualquier sitio de la terminal
echo -e "$GREEN[+]$RESTORE Creando alias de la aplicacion\n"
if [ -f ~/.aliases ]; then
	# Comprueba si existe ya un alias creado para este programa
	existe=`grep "notas.py" ~/.aliases`
	if [ $? -ne 0 ]; then
		echo 'alias notas="python '$EXECUTABLE_DIR'"' >> ~/.aliases
	fi
elif [ -f ~/.bash_aliases ]; then
	# Comprueba si existe ya un alias creado para este programa
	existe=`grep "notas.py" ~/.bash_aliases`
	if [ $? -ne 0 ]; then
		echo 'alias notas="python '$EXECUTABLE_DIR'"' >> ~/.bash_aliases
	fi
elif [ -f ~/.bashrc ]; then
	# Comprueba si existe ya un alias creado para este programa
	existe=`grep "notas.py" ~/.bashrc`
	if [ $? -ne 0 ]; then
		echo 'alias notas="python '$EXECUTABLE_DIR'"' >> ~/.bashrc
	fi
fi

# Si se va a usar el programa con un usuario que no sea root se han de cambiar
# los permisos de la carpeta donde se va a instalar
read -e -p "¿Vas a usar la aplicacion con un usuario sin privilegios? [s/n]: " opt
if [ "$opt" == "s" ]; then
	read -e -p "Usuario con el que se va a ejecutar: " username
	check_user=`cat /etc/passwd | cut -d':' -f1 | grep $username`
	if [ "$check_user" == "$username" ]; then 
		chown -R $username:$username $INSTALLATION_PROJECT
		echo -e "$GREEN[+]$RESTORE Permisos cambiados correctamente"
	else 
		echo -e "$RED[-]$RESTORE El usuario introducido no existe."
	fi
fi

echo -e "\n$GREEN[*]$RESTORE Instalacion completa creada en" $INSTALLATION_PROJECT 
echo -e "\n$LBLUE[!]$RESTORE Para ejecutar la aplicacion abre otra terminal y escribe notas\n"
