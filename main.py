import mysql.connector

conn = mysql.connector.connect(
    host="host",
    user="user",
    password="contraseña",
    database="agendar"
)


cursor = conn.cursor()
print("Bienvenido a")
print("AgendAR")
print("Un programa de Turnero \n")


def menu_principal():
    while True:
        print("1. Sacar turno")
        print("2. Mis Turnos")
        print("3. Lista de medicos")
        print("4. Info Hospital")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_turno()
        elif opcion == "2":
            listar_turnos()
        elif opcion == "3":
            vizualizar_medicos()
        elif opcion == "4":
            info_hospital()
        elif opcion == "0":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")


def registrar_turno():
    print("\n--- Registro de Turno ---")
    dni = input("DNI del paciente: ")

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

def listar_turnos():
    print("\n--- Mis Turnos ---")
    dni = input("DNI del paciente: ")

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


# Ejecutar menú
menu_principal()
