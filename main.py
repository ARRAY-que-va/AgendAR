import mysql.connector

import menus.paciente
import menus.medico
import menus.admin

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Myroot1235",
    database="agendar"
)

print(conn)

from datetime import datetime
cursor = conn.cursor()
print("Bienvenido a")
print("AgendAR")
print("Un programa de Turnero \n")

def iniciar_sistema():
    usuario = login()
    if usuario:
        id_usuario, rol = usuario
        if rol == "paciente":
            menu_paciente(id_usuario)
        elif rol == "medico":
            menu_medico(id_usuario)
        elif rol == "admin":
            menu_admin()
        else:
            print("Rol desconocido.")

def login():
    print("=== Inicio de Sesión ===")
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")

    cursor.execute("SELECT id_usuario, rol FROM usuarios WHERE usuario = %s AND contraseña = %s", (usuario, contrasena))
    resultado = cursor.fetchone()

    if resultado:
        print(f"Bienvenido {usuario} - Rol: {resultado[3]}")
        return resultado  # (id_usuario, rol)
    else:
        print("Credenciales incorrectas.\n")
        return None

# falta hacer la funcion def crear cuenta  
iniciar_sistema()

