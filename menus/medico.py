
# Menu
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

# Funciones
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