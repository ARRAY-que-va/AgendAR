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
    print("\n=== MENÚ Usuario ===")
    print("1. Iniciar sesion")
    print("2. Crear usuario ")
    opcion = input("Selecciona una opción: ")
    if opcion == "1":
        usuario = login()
    elif opcion == "2":
        usuario = crear_usuario()
        if usuario == None:
            iniciar_sistema()
        else:
            print("\n=== Felicitaciones ya creaste tu cuenta ===")
            print(" Iniciar sesion")
        usuario = login()
    else:
        print("Opción no válida. Intenta de nuevo.")
    if usuario:

        id_usuario, rol = usuario
        if rol == "paciente":
            menus.paciente.menu_paciente(conn, cursor,id_usuario)
        elif rol == "medico":
            menus.medico.menu_medico(conn, cursor,id_usuario)
        elif rol == "admin":
            menus.admin.menu_admin(conn, cursor)
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

# FUNCIÓN: crear_cuenta
def crear_usuario(conn, cursor): 
    print("\n=== Creación de Cuenta ===")
    nuevo_usuario = input("Define tu nombre de usuario: ")
    nueva_contrasena = input("Define tu contraseña: ")
    rol_defecto = "paciente"
    try:
        cursor.execute("SELECT id_user FROM user WHERE usuario = %s", (nuevo_usuario,))
        if cursor.fetchone():
            print("El nombre de usuario ya existe. Por favor, elige otro.")
            return
        cursor.execute("INSERT INTO user (usuario, pwd, rol) VALUES (%s, %s, %s)", (nuevo_usuario, nueva_contrasena, rol_defecto))
        conn.commit() 
        print("Cuenta de usuario creada con éxito.")
        cursor.execute("SELECT LAST_INSERT_ID()")
        id_usuario_reciente = cursor.fetchone()[0]
        if rol_defecto == "paciente":
            nombre_paciente = input("Tu nombre: ")
            apellido_paciente = input("Tu apellido: ")
            dni_paciente = input("Tu DNI: ") 
            email_paciente = input("Tu email (opcional): ")
            telefono_paciente = input("Tu teléfono (opcional): ")
            direccion_paciente = input("Tu dirección: ")
            cursor.execute("SELECT id_obrasocial, nombre FROM obrasocial")
            obras_sociales_disponibles = cursor.fetchall()
            print("\nObras Sociales disponibles:")
            for os_id, os_nombre in obras_sociales_disponibles:
                print(f"{os_id}. {os_nombre}")
            obrasocial_id_str = input("Selecciona el ID de tu obra social (dejar vacío si no tienes): ")
            obrasocial_id = int(obrasocial_id_str) if obrasocial_id_str.isdigit() else None
            cursor.execute("""
                INSERT INTO pacientes (nombre, apellido, user_id, dni, fecha_nacimiento, telefono, email, obrasocial_id, direccion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nombre_paciente, apellido_paciente, id_usuario_reciente, dni_paciente, None, telefono_paciente, email_paciente, obrasocial_id, direccion_paciente))
            conn.commit() 
            print("Datos de paciente guardados con éxito.")
        return (id_usuario_reciente)
    except mysql.connector.Error as err:
        print(f"Error al crear la cuenta: {err}")
        if conn:
            conn.rollback() 
        return (None)
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return (None)

iniciar_sistema()

