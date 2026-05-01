# Paquete de vistas: capa de presentación (interfaces de consola).
from controllers import (
    EmployeeController,
    LeaveTypeController,
    LeaveController,
    StatsController,
)


class Menu:
    def __init__(self):
        self.employee_controller   = EmployeeController()
        self.leave_type_controller = LeaveTypeController()
        self.leave_controller      = LeaveController()

    # Submenú CRUD de empleados.
    def employee_menu(self):
        while True:
            print("\n=== MENÚ EMPLEADOS ===")
            print("1. Registrar empleado")
            print("2. Listar empleados")
            print("3. Eliminar empleado")
            print("0. Volver")

            option = input("Opción: ")

            try:
                if option == "1":
                    self.employee_controller.create()
                elif option == "2":
                    self.employee_controller.read()
                elif option == "3":
                    self.employee_controller.delete()
                elif option == "0":
                    break
                else:
                    print("Opción inválida")
            except Exception as e:
                print("Error:", e)

    # Submenú CRUD de tipos de permiso.
    def leave_type_menu(self):
        while True:
            print("\n=== MENÚ TIPOS DE PERMISO ===")
            print("1. Registrar tipo de permiso")
            print("2. Listar tipos de permiso")
            print("3. Eliminar tipo de permiso")
            print("0. Volver")

            option = input("Opción: ")

            try:
                if option == "1":
                    self.leave_type_controller.create()
                elif option == "2":
                    self.leave_type_controller.read()
                elif option == "3":
                    self.leave_type_controller.delete()
                elif option == "0":
                    break
                else:
                    print("Opción inválida")
            except Exception as e:
                print("Error:", e)

    # Submenú CRUD de permisos.
    def leave_menu(self):
        while True:
            print("\n=== MENÚ PERMISOS ===")
            print("1. Registrar permiso")
            print("2. Listar permisos")
            print("3. Eliminar permiso")
            print("0. Volver")

            option = input("Opción: ")

            try:
                if option == "1":
                    self.leave_controller.create()
                elif option == "2":
                    self.leave_controller.read()
                elif option == "3":
                    self.leave_controller.delete()
                elif option == "0":
                    break
                else:
                    print("Opción inválida")
            except Exception as e:
                print("Error:", e)

    # Vista de estadísticas.
    def stats_view(self):
        StatsController().show()

    # Menú principal.
    def main_menu(self):
        while True:
            print("\n==============================")
            print(" SISTEMA DE PERMISOS ")
            print("==============================")
            print("1. Empleados")
            print("2. Tipos de Permiso")
            print("3. Permisos")
            print("4. Estadísticas")
            print("0. Salir")

            option = input("Opción: ")

            if option == "1":
                self.employee_menu()
            elif option == "2":
                self.leave_type_menu()
            elif option == "3":
                self.leave_menu()
            elif option == "4":
                self.stats_view()
            elif option == "0":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida")
