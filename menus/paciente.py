import mysql.connector

def menu_paciente(conn, cursor, id_usuario): 
    while True:
        print("\n--- Menú Paciente ---")
        print("1. Sacar turno")
        print("2. Mis Turnos")
        print("3. Lista de médicos")
        print("4. Info Hospital")
        print("0. Salir")

        opcion = input("Opción: ")
        if opcion == "1":
            registrar_turno(conn, cursor, id_usuario) 
        elif opcion == "2":
            listar_turnos(cursor, id_usuario) 
        elif opcion == "3":
            vizualizar_medicos(cursor) 
        elif opcion == "4":
            info_hospital() 
        elif opcion == "0":
            print("Cerrando sesión del paciente...\n")
            break
        else:
            print("Opción inválida.")

def registrar_turno(conn, cursor, id_usuario): 
    print("\n--- Registro de Turno ---")
    cursor.execute("SELECT id_paciente, nombre, apellido FROM pacientes WHERE user_id = %s", (id_usuario,))
    paciente = cursor.fetchone()
    if not paciente:
        print("Paciente no registrado en la tabla de pacientes. Por favor, contacta al administrador.")
        return
    print(f"Hola Paciente: {paciente[1]} {paciente[2]}")
    cursor.execute("""
        SELECT m.id_medico, m.nombre, m.apellido, e.nombre
        FROM medicos m
        JOIN especialidades e ON m.especialidad_id = e.id_especialidad
    """)
    medicos = cursor.fetchall()
    if not medicos:
        print("No hay médicos disponibles para asignar turnos.")
        return
    print("\nMédicos disponibles:")
    for med in medicos:
        print(f"{med[0]}. {med[1]} {med[2]} - Especialidad: {med[3]}")
    id_medico = input("Selecciona el ID del médico: ")
    fecha = input("Fecha del turno (YYYY-MM-DD): ")
    hora = input("Hora del turno (HH:MM): ")
    try:
        cursor.execute("SELECT COUNT(*) FROM turnos WHERE medico_id = %s AND fecha = %s AND hora = %s", (id_medico, fecha, hora))
        if cursor.fetchone()[0] > 0:
            print("Lo sentimos, el médico ya tiene un turno agendado para esa fecha y hora.")
            return
        cursor.execute("""
            INSERT INTO turnos (paciente_id, medico_id, fecha, hora, estado)
            VALUES (%s, %s, %s, %s, 'pendiente')
        """, (paciente[0], id_medico, fecha, hora))
        conn.commit()
        print("Turno registrado con éxito. Estado: Pendiente.")
    except mysql.connector.Error as err:
        print("Error al registrar el turno:", err)
        conn.rollback() # Deshacer en caso de error
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


def listar_turnos(cursor, id_usuario):
    print("\n--- Mis Turnos ---")
    cursor.execute("""
        SELECT p.id_paciente, p.nombre, p.apellido FROM pacientes p WHERE user_id = %s
    """, (id_usuario,))
    paciente = cursor.fetchone()
    if not paciente:
        print("Paciente no registrado en la tabla de pacientes.")
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
        print("No hay turnos registrados para este paciente.")
        return
    for t in turnos:
        print(f"{t[0]} a las {t[1]} hs - Dr. {t[3]} {t[4]} ({t[5]}) - Estado: {t[2]}")

def vizualizar_medicos(cursor): 
    print("\n--- Lista de Médicos ---")
    cursor.execute("""
        SELECT m.nombre, m.apellido, m.matricula, e.nombre, c.piso, c.area, c.sala
        FROM medicos m
        JOIN especialidades e ON m.especialidad_id = e.id_especialidad
        JOIN consultorio c ON m.consultorio_id = c.id_consultorio
    """)
    medicos = cursor.fetchall()
    if not medicos:
        print("No hay médicos registrados en el sistema.")
        return
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