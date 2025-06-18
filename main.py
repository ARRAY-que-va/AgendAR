import mysql.connector

import menus.paciente
import menus.medico
import menus.admin

#Coneccion con la base
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Myroot1235",
    database="agendar"
)
print(conn)

#Texto de bienvenida
from datetime import datetime
cursor = conn.cursor()
print("Bienvenido a")
print("AgendAR")
print("Un programa de Turnero \n")

#Lo primero es la fucion que ve que tipo de usuario es, sin antes logear
def iniciar_sistema():
    usuario = login()
    if usuario:
        id_usuario, rol = usuario
        if rol == "paciente":
            menus.paciente.menu_paciente(id_usuario)
        elif rol == "medico":
            menus.medico.menu_medico(id_usuario)
        elif rol == "admin":
            menus.admin.menu_admin()
        else:
            print("Rol desconocido.")

#Es la fucion para  logear
def login():
    print("=== Inicio de Sesión ===")
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")

    cursor.execute("SELECT id_user, rol FROM user WHERE usuario = %s AND pwd = %s", (usuario, contrasena))
    resultado = cursor.fetchone()

    if resultado:
        print(f"Bienvenido {usuario} - Rol: {resultado[1]}")
        return resultado  
    else:
        print("Credenciales incorrectas.\n")
        return None

# falta hacer la funcion def crear cuenta  
iniciar_sistema()

