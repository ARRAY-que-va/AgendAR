import mysql.connector

def menu_admin(conn, cursor): 
    while True:
        print("\n=== MENÚ ADMINISTRADOR ===")
        print("1. Gestionar Roles")
        print("2. Gestionar Usuarios")
        print("3. Ver todos los turnos")
        print("4. Gestionar Turnos")
        print("0. Cerrar sesión")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            gestionar_roles(conn, cursor) 
        elif opcion == "2":
            gestionar_usuarios(conn, cursor) 
        elif opcion == "3":
            ver_todos_los_turnos(cursor) 
        elif opcion == "4":
            gestionar_turnos(conn, cursor) 
        elif opcion == "0":
            print("Cerrando sesión del administrador...\n")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

#Poder Cambiar configuraciones de Un usuario
def gestionar_roles(conn, cursor): 
    while True:
        print("\n--- CAMBIAR ROL DE USUARIOS ---")
        print("1. Ver usuarios y sus roles")
        print("2. Cambiar rol de un usuario")
        print("0. Volver al menú admin")
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            ver_usuarios_y_roles(cursor) 
        elif opcion == "2":
            cambiar_rol_de_usuario(conn, cursor) 
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")




def ver_usuarios_y_roles(cursor): 
    cursor.execute("""
        SELECT id_user, usuario, rol
        FROM user 
    """)
    usuarios = cursor.fetchall()
    print("\n--- Usuarios y sus roles ---")
    for u in usuarios:
        print(f"ID: {u[0]} | Usuario: {u[1]} | Rol: {u[2]}")

def cambiar_rol_de_usuario(conn, cursor):
    id_usuario = input("ID del usuario a modificar: ")
    print("Roles disponibles:")
    print("medico, paciente, admin:")
    
    nuevo_rol = input("Nuevo rol: ")
    try:
        cursor.execute("UPDATE user SET rol = %s WHERE id_user = %s", (nuevo_rol, id_usuario))
        conn.commit()
        print("Rol actualizado correctamente.")
    except Exception as e:
        print(f"Error al cambiar el rol: {e}")
        conn.rollback()

def gestionar_usuarios(conn, cursor): 
    while True:
        print("\n--- GESTIONAR USUARIOS ---")
        print("1. Ver todos los usuarios")
        print("2. Modificar un usuario")
        print("3. Eliminar un usuario")
        print("0. Volver al menú admin")
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            ver_todos_los_usuarios(cursor) 
        elif opcion == "2":
            modificar_usuario(conn, cursor) 
        elif opcion == "3":
            eliminar_usuario(conn, cursor) 
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

def ver_todos_los_usuarios(cursor): 
    print("\n--- Lista de Usuarios ---")
    cursor.execute("SELECT id_user, usuario, rol FROM user")
    usuarios = cursor.fetchall()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    for u in usuarios:
        print(f"ID: {u[0]} | Usuario: {u[1]} | Rol: {u[2]}")

def modificar_usuario(conn, cursor): 
    print("\n--- Modificar Usuario ---")
    id_usuario = input("Ingrese el ID del usuario a modificar: ")
    cursor.execute("SELECT usuario, rol FROM user WHERE id_user = %s", (id_usuario,))
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
            try:
                cursor.execute("UPDATE user SET usuario = %s WHERE id_user = %s", (nuevo_usuario, id_usuario))
                conn.commit()
                print("Nombre de usuario actualizado.")
                usuario = (nuevo_usuario, usuario[1])
            except Exception as e:
                print(f"Error al actualizar nombre de usuario: {e}")
                conn.rollback()
        elif opcion == "2":
            nueva_contrasena = input("Nueva contraseña: ")
            try:
                cursor.execute("UPDATE user SET pwd = %s WHERE id_user = %s", (nueva_contrasena, id_usuario))
                conn.commit()
                print("Contraseña actualizada.")
            except Exception as e:
                print(f"Error al actualizar contraseña: {e}")
                conn.rollback()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")

def eliminar_usuario(conn, cursor): 
    print("\n--- Eliminar Usuario ---")
    id_usuario = input("Ingrese el ID del usuario a eliminar: ")
    cursor.execute("SELECT usuario, rol FROM user WHERE id_user = %s", (id_usuario,))
    usuario = cursor.fetchone()
    if not usuario:
        print("Usuario no encontrado.")
        return
    confirmacion = input(f"¿Estás seguro de eliminar al usuario '{usuario[0]}'? (s/n): ")
    if confirmacion.lower() == "s":
        try:
            if usuario[1] == "medico":
                cursor.execute("DELETE FROM medico WHERE user_id = %s", (id_usuario,))
            if usuario[1] == "paciente":
                cursor.execute("DELETE FROM pacientes WHERE user_id = %s", (id_usuario,))
            cursor.execute("DELETE FROM user WHERE id_user = %s", (id_usuario,))
            conn.commit()
            print("Usuario eliminado con éxito.")
        except mysql.connector.Error as err:
            print("Error al eliminar el usuario:", err)
            conn.rollback()
    else:
        print("Eliminación cancelada.")

def gestionar_turnos(conn, cursor): 
    while True:
        print("\n--- GESTIONAR TURNOS ---")
        print("1. Crear turno")
        print("2. Modificar turno")
        print("3. Eliminar turno")
        print("0. Volver al menú admin")

        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            crear_turno_admin(conn, cursor)
        elif opcion == "2":
            modificar_turno(conn, cursor)
        elif opcion == "3":
            eliminar_turno(conn, cursor)
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

def crear_turno_admin(conn, cursor): 
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
        conn.rollback()

def modificar_turno(conn, cursor): 
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
        try:
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
        except Exception as e:
            print(f"Error al modificar el turno: {e}")
            conn.rollback()

def eliminar_turno(conn, cursor): 
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
            conn.rollback()
    else:
        print("Eliminación cancelada.")

def ver_todos_los_turnos(cursor): 
    print("\n--- TODOS LOS TURNOS ---")
    cursor.execute("""
        SELECT t.id_turno, t.fecha, t.hora, t.estado, p.nombre, p.apellido, m.nombre
        FROM turnos t
        JOIN pacientes p ON t.paciente_id = p.id_paciente
        JOIN medicos m ON t.medico_id = m.id_medico
        ORDER BY t.fecha, t.hora
    """)
    turnos = cursor.fetchall()
    if not turnos:
        print("No hay turnos registrados en el sistema.")
        return
    for t in turnos:
            # 0 = fecha 1 = HORA 2 = ESTADO 3 = NOMBRE 4 = APELLIDO 5 = MEDICO
        print(f"ID: {t[0]} | {t[1]} {t[2]} | Estado: {t[3]} | Paciente: {t[4]} {t[5]} | Médico: {t[6]}")