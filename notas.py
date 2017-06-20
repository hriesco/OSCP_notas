#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path, listdir, system, popen, makedirs, remove
from termcolor import colored
import subprocess
import shutil
import signal
import git
import sys

PATH=path.dirname(path.abspath(__file__)) # Absolute path
DIR_NOTES=PATH+"/Notas" # Directory where are the notes modules

def cls():
    system("clear")

# Check if pressed Ctrl + C
def signal_handler(signal, frame):
    sys.exit(0)

def title():
    cls()
    print colored('░█▀█░█▀▀░█▀▀░█▀█░░░█▀█░█▀█░▀█▀░█▀▀░█▀▀', 'green')
    print colored('░█░█░▀▀█░█░░░█▀▀░░░█░█░█░█░░█░░█▀▀░▀▀█', 'green')
    print colored('░▀▀▀░▀▀▀░▀▀▀░▀░░░░░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀', 'green')
    print

# For each note file parse _ and .txt
def parse_file(index, file_name):
    filename = file_name.replace('.txt','')
    words_array = filename.split("[")
    module_array1 = words_array[0].split("_")
    s = str(index+1) + ") " + module_array1[0]
    for i in range(1, len(module_array1)):
        if module_array1[i]: 
            s += " " + module_array1[i]

    if len(words_array) > 1:
        module_array2 = words_array[1].split("_")
        s += colored(" [", "red") + colored(module_array2[0], "red")
        for i in range(1, len(module_array2)):
            if module_array2[i]: 
                s += " " + colored(module_array2[i], 'red')

    return s

# For each module parse NAME_PORTS
def parse_module(index, module_name):
    module_array = module_name.split("_")
    s = str(index+1) + ") " + module_array[0] + " ["
    for i in range(1, len(module_array)):
        if i != 1 and i != len(module_array):
            s += ", " +  colored(module_array[i], 'red')
        else:
            s += colored(module_array[i], 'red')
    s += "]"
    return s

# Show a file paged with terminal height
def pagetext(text_line, num_lines):
   for index, line in enumerate(text_line):
       if index % (num_lines - 1) == 0 and index:
           msg = colored("Pulsa Enter para continuar o q para salir", "green")
           opc = raw_input(msg)
           if opc.lower() == 'q':
               break
       else:
            if line[0] == '#':
                sys.stdout.write(colored(line, 'blue')) 
            else:
                sys.stdout.write(line)

# Show file in terminal 
def cat_file(filename):
    if path.exists(filename):
        cls()
        rows, columns = popen('stty size', 'r').read().split()
        with open(filename, 'r') as outFile:
            pagetext(outFile, int(rows))
    else:
        print "No existe el fichero" + filename 

# Generate a menu with an array of items
def list_menu(items, tipo=""):
    title()

    if tipo == "modules":
        for i, opt in enumerate(items):
            print parse_module(i, opt)
    elif tipo == "files":
        for i, opt in enumerate(items):
            print parse_file(i, opt)
    else:
        for i, opt in enumerate(items):
            print str(i+1) + ") " + opt

    if tipo == "exit":
        print "0) Exit\n"
    elif tipo != "notzero": 
        print "0) Back\n"
    else:
        print "\n"

    opc = -1
    while opc < 0 or opc > len(items):
        opc = raw_input("Opc > ")
        if not opc or not opc.isdigit(): 
            opc = -1
        else:
            opc = int(opc)

    return opc

# List all files inside a module directory 
def list_files(directory):
    full_dir = DIR_NOTES + "/" + directory
    full_file = None
    if path.exists(full_dir):
        files = listdir(full_dir)
        files = sorted(files)
        opc = list_menu(files, "files")

        if opc != 0:
            full_file = full_dir + "/" + files[opc-1]
    else:
        print "No existe el directorio " + full_dir 

    return full_file

# List all directory modules inside Notas
def list_modules():
    module = None
    if path.exists(DIR_NOTES):
        directories = listdir(DIR_NOTES)
        directories = sorted(directories)
        opc = list_menu(directories, "modules") 

        if opc != 0:
            module = directories[opc-1]
    else:
        print "No existe el directorio " + DIR_NOTES 

    return module

# Add a module to Notas directory
def add_module():
    print "Recuerda escribir el nombre del modulo con el siguiente formato:"
    print "NOMBRE-SERVICIO_PUERTO1_PUERTO2\n"
    name = raw_input("Nombre modulo: ")
    try:
        full_dir = DIR_NOTES + "/" + name
        if path.exists(full_dir):
            text=raw_input("Ya existe un directorio con ese nombre...\n")
        else:
            makedirs(full_dir)
            text=raw_input("\nModulo creado! Pulse Enter para continuar...")
    except OSError:
        print "Error al crear el directorio"

# Add a note from a module passed as a parameter
def add_note(module):
    name = raw_input("Nombre de la nota: ")
    full_file = DIR_NOTES + "/" + module + "/" + name
    if path.exists(full_file):
        print "El fichero ya existe"
    else:
        f = open (full_file, 'w')
        f.close()	
        
        items = ['gedit', 'vim', 'nano']
        items = sorted(items)
        opc = list_menu(items, "notzero")

        proc = subprocess.Popen([items[opc-1], full_file])	
        proc.wait()
        list_options()


# Function that handles add a module or a note
def add_module_or_note():
    items = ['Modulo', 'Nota']
    items = sorted(items)
    opc = list_menu(items)

    if opc == 1:
        title()
        add_module()
        list_options()
    elif opc == 2:
        module = list_modules() 
        if module != None:
            add_note(module)
        else:
            add_module_or_note()
    elif opc == 0:
        list_options()

# Delete a module
def delete_module():
    module = list_modules()
    if module != None:
        full_dir = DIR_NOTES + "/" + module
        shutil.rmtree(full_dir)
        text = raw_input("\nModulo borrado! Pulse Enter para continuar...")
        list_options()
    else:
        delete_module_or_note()

# Delete a note from a module
def delete_note():
    module = list_modules()
    if module != None:
        filename = list_files(module)
        if filename != None:
            remove(filename)
            text = raw_input("\nFichero borrado! Pulse Enter para continuar...")
            list_options()
        else:
            delete_note()
    else:
        delete_module_or_note()

# Delete module or a note 
def delete_module_or_note():
    items = ['Borrar Modulo', 'Borrar Nota']
    items = sorted(items)
    opc = list_menu(items)
    
    if opc == 1:
        delete_module()
    elif opc == 2:
        delete_note()
    elif opc == 0:
        list_options()

# Edit one note from a module
def edit_note():
    module = list_modules()
    if module:
        filename = list_files(module)
        if filename != None:
            items = ['gedit', 'vim', 'nano']
            items = sorted(items)
            opc = list_menu(items, "notzero")

            proc = subprocess.Popen([items[opc-1], filename])	
            proc.wait()
            list_options()
        else:
            edit_note()
    else:
        list_options()

# Function that handles viewing a module note
def view_note():
    module = list_modules()
    if module != None:
        file = list_files(module)
        if file != None:
            cat_file(file)
            msg = colored("Pulsa Enter para ir al menu", "green")
            input = raw_input(msg)
            list_options()
        else:
            view_note()
    else:
        list_options()

# Function to download last changes from Git
def update():
    repo = git.Repo(PATH)
    print repo.git.pull('origin', 'master')

# Function to upload last changes to Git
def upload():
    repo = git.Repo(PATH)
    print repo.git.add('*')
    commit = raw_input("Escribe menaje para el commit: ")
    print repo.git.commit(m=commit)
    print repo.git.status()
    print repo.git.push()
    list_options()

# Principal menu with the basic operations
def list_options():
    items = ['Ver', 'Añadir', 'Editar', 'Borrar', 'Actualizar', 'Subir a Git']
    opc = list_menu(items, "exit") 

    if opc == 1:
        view_note()
    elif opc == 2:
        add_module_or_note()
    elif opc == 3:
        edit_note()
    elif opc == 4:
        delete_module_or_note()
    elif opc == 5:
        update()
    elif opc == 6:
        upload()

# Main
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    list_options()

