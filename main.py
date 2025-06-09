import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="tu_usuario",
    password="tu_contraseña",
    database="agendar"
)

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


            def listar_turnos():


            def vizualizar_medicos():


            def info_hospital():