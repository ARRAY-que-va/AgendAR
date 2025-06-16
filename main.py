import mysql.connector

conn = mysql.connector.connect(
    host="host",
    user="user",
    password="contraseña",
    database="agendar"
)
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
        print(f"Bienvenido {usuario} - Rol: {resultado[1]}")
        return resultado  # (id_usuario, rol)
    else:
        print("Credenciales incorrectas.\n")
        return None

# falta hacer la funcion def crear cuenta  

def menu_paciente(id_usuario):
    while True:
        print("\n--- Menú Paciente ---")
        print("1. Sacar turno")
        print("2. Mis Turnos")
        print("3. Lista de médicos")
        print("4. Info Hospital")
        print("0. Salir")

        opcion = input("Opción: ")
        if opcion == "1":
            registrar_turno(id_usuario)
        elif opcion == "2":
            listar_turnos(id_usuario)
        elif opcion == "3":
            vizualizar_medicos()
        elif opcion == "4":
            info_hospital()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")

def menu_medico(usuario_id):
    while True:
        print("\n--- Menú Médico ---")
        print("1. Ver mis turnos")
        print("0. Salir")

        opcion = input("Opción: ")
        if opcion == "1":
            ver_turnos_medico(usuario_id)
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")

def menu_admin():
    while True:
        print("\n=== MENÚ ADMINISTRADOR ===")
        print("1. Gestionar Roles")
        print("2. Gestionar Usuarios")
        print("3. Ver todos los turnos")
        print("4. Gestionar Turnos")
        print("0. Cerrar sesión")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            gestionar_roles()
        elif opcion == "2":
            gestionar_usuarios()
        elif opcion == "3":
            ver_todos_los_turnos()
        elif opcion == "4":
            gestionar_turnos()
        elif opcion == "0":
            print("Cerrando sesión del administrador...\n")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")
# Funciones del menu paciente  

def registrar_turno(id_usuario):
    print("\n--- Registro de Turno ---")
    dni = id_usuario

    cursor.execute("SELECT id_paciente, nombre, apellido FROM pacientes WHERE dni = %s", (dni,))
    paciente = cursor.fetchone()

    if not paciente:
        print("Paciente no registrado.")
        return

    print(f"Hola Paciente: {paciente[1]} {paciente[2]}")
    cursor.execute("""
        SELECT m.id_medico, m.nombre, m.apellido, e.nombre 
        FROM medicos m
        JOIN especialidades e ON m.especialidad_id = e.id_especialidad
""")
    medicos = cursor.fetchall()
    for med in medicos:
        print(f"{med[0]}. {med[1]} {med[2]} - Especialidad: {med[3]}")

    id_medico = input("Selecciona el ID del médico: ")
    fecha = input("Fecha del turno (YYYY-MM-DD): ")
    hora = input("Hora del turno (HH:MM): ")

    try:


        # aca falta validacion si hay turno disponible o si no hay 


        cursor.execute("""
            INSERT INTO turnos (paciente_id, medico_id, fecha, hora)
            VALUES (%s, %s, %s, %s)
        """, (paciente[0], id_medico, fecha, hora))
        conn.commit()

        print("Turno registrado con éxito.")
    except mysql.connector.Error as err:
        print("Error al registrar el turno:", err)

def listar_turnos(id_usuario):
    print("\n--- Mis Turnos ---")
    dni = id_usuario

    cursor.execute("""
        SELECT p.id_paciente, p.nombre, p.apellido FROM pacientes p WHERE dni = %s
    """, (dni,))
    paciente = cursor.fetchone()

    if not paciente:
        print("Paciente no registrado.")
        return

    cursor.execute("""
        SELECT t.fecha, t.hora, t.estado, m.nombre, m.apellido, e.nombre
        FROM turnos t
        JOIN medicos m ON t.medico_id = m.id_medico
        JOIN especialidades e ON m.especialidad_id = e.id_especialidad
        WHERE t.paciente_id = %s
        ORDER BY t.fecha, t.hora
    """, (paciente[0],))

    turnos = cursor.fetchall()

    if not turnos:
        print("No hay turnos registrados.")
        return

    for t in turnos:
        print(f"{t[0]} a las {t[1]} hs - Dr. {t[3]} {t[4]} ({t[5]}) - Estado: {t[2]}")

def vizualizar_medicos():
    print("\n--- Lista de Médicos ---")

    cursor.execute("""
        SELECT m.nombre, m.apellido, m.matricula, e.nombre, c.piso, c.área, c.sala
        FROM medicos m
        JOIN especialidades e ON m.especialidad_id = e.id_especialidad
        JOIN consultorio c ON m.consultorio_id = c.id_consultorio
    """)

    medicos = cursor.fetchall()

    for m in medicos:
        print(f"Dr. {m[0]} {m[1]} - Matrícula: {m[2]} - Especialidad: {m[3]}")
        print(f"  Consultorio: Piso {m[4]}, Área {m[5]}, Sala {m[6]}\n")

def info_hospital():
    print("\n--- Info del Hospital ---")
    print("Nombre: Hospital Central AgendAR")
    print("Dirección: Argentina")
    print("Teléfono: 08000000")
    print("Email: contacto@agendar.com.ar")
    print("Horario: Lunes a Viernes de 8:00 a 18:00 hs")

# Funciones del menu Medico

def ver_turnos_medico(usuario_id):
    cursor.execute("SELECT id_medico FROM medicos WHERE usuario_id = %s", (usuario_id,))
    medico = cursor.fetchone()

    if not medico:
        print("No se encontró al médico.")
        return

    cursor.execute("""
        SELECT t.fecha, t.hora, t.estado, p.nombre, p.apellido
        FROM turnos t
        JOIN pacientes p ON t.paciente_id = p.id_paciente
        WHERE t.medico_id = %s
        ORDER BY t.fecha, t.hora
    """, (medico[0],))

    turnos = cursor.fetchall()
    if not turnos:
        print("No hay turnos asignados.")
        return

    for t in turnos:
        # 0 = fecha 1 = HORA 2 = ESTADO 3 = NOMBRE 4 = APELLIDO
        print(f"{t[0]} {t[1]} - Paciente: {t[3]} {t[4]} - Estado: {t[2]}")

# Funciones del menu ADMIN    

def gestionar_roles():
    while True:
        print("\n--- CAMBIAR ROL DE USUARIOS ---")
        print("1. Ver usuarios y sus roles")
        print("2. Cambiar rol de un usuario")
        print("0. Volver al menú admin")
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            ver_usuarios_y_roles()
        elif opcion == "2":
            cambiar_rol_de_usuario()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

def mostrar_roles():
    cursor.execute("SELECT id_rol, nombre FROM roles")
    roles = cursor.fetchall()
    for r in roles:
        print(f"ID: {r[0]} | Rol: {r[1]}")

def ver_usuarios_y_roles():
    cursor.execute("""
        SELECT u.id_usuario, u.username, r.nombre
        FROM usuarios u
        JOIN roles r ON u.rol_id = r.id_rol
    """)
    usuarios = cursor.fetchall()
    print("\n--- Usuarios y sus roles ---")
    for u in usuarios:
        print(f"ID: {u[0]} | Usuario: {u[1]} | Rol: {u[2]}")

def cambiar_rol_de_usuario():
    id_usuario = input("ID del usuario a modificar: ")
    print("Roles disponibles:")
    mostrar_roles()
    nuevo_rol_id = input("Nuevo rol (ingresa el ID del rol): ")

    cursor.execute("UPDATE usuarios SET rol_id = %s WHERE id_usuario = %s", (nuevo_rol_id, id_usuario))
    print("Rol actualizado correctamente.")

def gestionar_usuarios():
    while True:
        print("\n--- GESTIONAR USUARIOS ---")
        print("1. Ver todos los usuarios")
        print("2. Modificar un usuario")
        print("3. Eliminar un usuario")
        print("0. Volver al menú admin")
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            ver_todos_los_usuarios()
        elif opcion == "2":
            modificar_usuario()
        elif opcion == "3":
            eliminar_usuario()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

def ver_todos_los_usuarios():
    print("\n--- Lista de Usuarios ---")
    cursor.execute("SELECT id_usuario, usuario, rol FROM usuarios")
    usuarios = cursor.fetchall()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    for u in usuarios:
        print(f"ID: {u[0]} | Usuario: {u[1]} | Rol: {u[2]}")

def modificar_usuario():
    print("\n--- Modificar Usuario ---")
    id_usuario = input("Ingrese el ID del usuario a modificar: ")
    cursor.execute("SELECT usuario, rol FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    usuario = cursor.fetchone()
    if not usuario:
        print("Usuario no encontrado.")
        return
    while True:
        print(f"\nUsuario actual: {usuario[0]} | Rol actual: {usuario[1]}")
        print("¿Qué desea modificar?")
        print("1. Nombre de usuario")
        print("2. Contraseña")
        print("0. Volver")
        opcion = input("Opción: ")
        if opcion == "1":
            nuevo_usuario = input("Nuevo nombre de usuario: ")
            cursor.execute("UPDATE usuarios SET usuario = %s WHERE id_usuario = %s", (nuevo_usuario, id_usuario))
            conn.commit()
            print("Nombre de usuario actualizado.")
            usuario = (nuevo_usuario, usuario[1]) 
        elif opcion == "2":
            nueva_contrasena = input("Nueva contraseña: ")
            cursor.execute("UPDATE usuarios SET contraseña = %s WHERE id_usuario = %s", (nueva_contrasena, id_usuario))
            conn.commit()
            print("Contraseña actualizada.")
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")

def eliminar_usuario():
    print("\n--- Eliminar Usuario ---")
    id_usuario = input("Ingrese el ID del usuario a eliminar: ")
    cursor.execute("SELECT usuario FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    usuario = cursor.fetchone()
    if not usuario:
        print("Usuario no encontrado.")
        return
    confirmacion = input(f"¿Estás seguro de eliminar al usuario '{usuario[0]}'? (s/n): ")
    if confirmacion.lower() == "s":
        try:
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            conn.commit()
            print("Usuario eliminado con éxito.")
        except mysql.connector.Error as err:
            print("Error al eliminar el usuario:", err)
    else:
        print("Eliminación cancelada.")

def gestionar_turnos():
    print("\n--- GESTIONAR TURNOS ---")
    print("1. Crear turno")
    print("2. Modificar turno")
    print("3. Eliminar turno")

def crear_turno_admin():
    print("\n--- Crear Turno ---")
    paciente_id = input("ID del paciente: ")
    medico_id = input("ID del médico: ")
    fecha = input("Fecha (YYYY-MM-DD): ")
    hora = input("Hora (HH:MM): ")

    try:
        cursor.execute("""
            INSERT INTO turnos (paciente_id, medico_id, fecha, hora)
            VALUES (%s, %s, %s, %s)
        """, (paciente_id, medico_id, fecha, hora))
        conn.commit()
        print("Turno creado con éxito.")
    except mysql.connector.Error as err:
        print("Error al crear el turno:", err)

def modificar_turno():
    print("\n--- Modificar Turno ---")
    id_turno = input("Ingrese el ID del turno a modificar: ")

    cursor.execute("""
        SELECT fecha, hora, estado, paciente_id, medico_id 
        FROM turnos WHERE id_turno = %s
    """, (id_turno,))
    turno = cursor.fetchone()

    if not turno:
        print("Turno no encontrado.")
        return

    while True:
        print(f"""
                Turno actual:
                - Fecha: {turno[0]}
                - Hora: {turno[1]}
                - Estado: {turno[2]}
                - ID Paciente: {turno[3]}
                - ID Médico: {turno[4]}
                """)
        print("¿Qué desea modificar?")
        print("1. Fecha")
        print("2. Hora")
        print("3. Estado")
        print("4. Paciente (ID)")
        print("5. Médico (ID)")
        print("0. Volver")

        opcion = input("Opción: ")

        if opcion == "1":
            nueva_fecha = input("Nueva fecha (YYYY-MM-DD): ")
            cursor.execute("UPDATE turnos SET fecha = %s WHERE id_turno = %s", (nueva_fecha, id_turno))
            conn.commit()
            turno = (nueva_fecha, turno[1], turno[2], turno[3], turno[4])
            print("Fecha actualizada.")

        elif opcion == "2":
            nueva_hora = input("Nueva hora (HH:MM): ")
            cursor.execute("UPDATE turnos SET hora = %s WHERE id_turno = %s", (nueva_hora, id_turno))
            conn.commit()
            turno = (turno[0], nueva_hora, turno[2], turno[3], turno[4])
            print("Hora actualizada.")

        elif opcion == "3":
            nuevo_estado = input("Nuevo estado (pendiente/confirmado/cancelado): ")
            if nuevo_estado not in ["pendiente", "confirmado", "cancelado"]:
                print("Estado inválido.")
            else:
                cursor.execute("UPDATE turnos SET estado = %s WHERE id_turno = %s", (nuevo_estado, id_turno))
                conn.commit()
                turno = (turno[0], turno[1], nuevo_estado, turno[3], turno[4])
                print("Estado actualizado.")

        elif opcion == "4":
            nuevo_paciente_id = input("Nuevo ID del paciente: ")
            cursor.execute("UPDATE turnos SET paciente_id = %s WHERE id_turno = %s", (nuevo_paciente_id, id_turno))
            conn.commit()
            turno = (turno[0], turno[1], turno[2], nuevo_paciente_id, turno[4])
            print("ID del paciente actualizado.")

        elif opcion == "5":
            nuevo_medico_id = input("Nuevo ID del médico: ")
            cursor.execute("UPDATE turnos SET medico_id = %s WHERE id_turno = %s", (nuevo_medico_id, id_turno))
            conn.commit()
            turno = (turno[0], turno[1], turno[2], turno[3], nuevo_medico_id)
            print("ID del médico actualizado.")

        elif opcion == "0":
            break
        else:
            print("Opción inválida.")

def eliminar_turno():
    print("\n--- Eliminar Turno ---")
    id_turno = input("ID del turno a eliminar: ")

    cursor.execute("SELECT id_turno FROM turnos WHERE id_turno = %s", (id_turno,))
    if not cursor.fetchone():
        print("Turno no encontrado.")
        return

    confirmacion = input("¿Estás seguro de eliminar el turno? (s/n): ")
    if confirmacion.lower() == "s":
        try:
            cursor.execute("DELETE FROM turnos WHERE id_turno = %s", (id_turno,))
            conn.commit()
            print("Turno eliminado con éxito.")
        except mysql.connector.Error as err:
            print("Error al eliminar el turno:", err)
    else:
        print("Eliminación cancelada.")

def ver_todos_los_turnos():
    print("\n--- TODOS LOS TURNOS ---")
    cursor.execute("""
        SELECT t.fecha, t.hora, t.estado, p.nombre, p.apellido, m.nombre
        FROM turnos t
        JOIN pacientes p ON t.paciente_id = p.id_paciente
        JOIN medicos m ON t.medico_id = m.id_medico
        ORDER BY t.fecha, t.hora
    """)
    turnos = cursor.fetchall()
    for t in turnos:
            # 0 = fecha 1 = HORA 2 = ESTADO 3 = NOMBRE 4 = APELLIDO 5 = MEDICO
        print(f"{t[0]} {t[1]} | Estado: {t[2]} | Paciente: {t[3]} {t[4]} | Médico: {t[5]}")

iniciar_sistema()