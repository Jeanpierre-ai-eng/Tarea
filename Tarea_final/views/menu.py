# Paquete de vistas: capa de presentación (interfaces de consola).
from controllers import (
    EmployeeController,
    LeaveTypeController,
    LeaveController,
    StatsController,
)
from core import (
    clear,
    print_header,
    print_separator,
    print_option,
    print_warning,
    print_error,
    Color,
)


class Menu:
    def __init__(self):
        self.employee_controller   = EmployeeController()
        self.leave_type_controller = LeaveTypeController()
        self.leave_controller      = LeaveController()

    # ── Submenú CRUD de empleados ─────────────────────────────────────────────
    def employee_menu(self):
        while True:
            clear()
            print_header("MENÚ EMPLEADOS")
            print_option("1", "Registrar empleado", Color.BG_GREEN,  Color.BGREEN)
            print_option("2", "Listar empleados",   Color.BG_CYAN,   Color.BCYAN)
            print_option("3", "Eliminar empleado",  Color.BG_RED,    Color.BRED)
            print_option("0", "Volver",             Color.BG_YELLOW, Color.BYELLOW)
            print_separator()

            option = input(Color.paint("  Opción: ", Color.BOLD, Color.BWHITE))

            try:
                if option == "1":
                    clear()
                    self.employee_controller.create()
                elif option == "2":
                    clear()
                    self.employee_controller.read()
                elif option == "3":
                    clear()
                    self.employee_controller.delete()
                elif option == "0":
                    break
                else:
                    print_warning("Opción inválida")
            except Exception as e:
                print_error(str(e))

            input(Color.paint("\n  Presione Enter para continuar...", Color.BYELLOW))

    # ── Submenú CRUD de tipos de permiso ──────────────────────────────────────
    def leave_type_menu(self):
        while True:
            clear()
            print_header("MENÚ TIPOS DE PERMISO")
            print_option("1", "Registrar tipo de permiso", Color.BG_GREEN,  Color.BGREEN)
            print_option("2", "Listar tipos de permiso",   Color.BG_CYAN,   Color.BCYAN)
            print_option("3", "Eliminar tipo de permiso",  Color.BG_RED,    Color.BRED)
            print_option("0", "Volver",                    Color.BG_YELLOW, Color.BYELLOW)
            print_separator()

            option = input(Color.paint("  Opción: ", Color.BOLD, Color.BWHITE))

            try:
                if option == "1":
                    clear()
                    self.leave_type_controller.create()
                elif option == "2":
                    clear()
                    self.leave_type_controller.read()
                elif option == "3":
                    clear()
                    self.leave_type_controller.delete()
                elif option == "0":
                    break
                else:
                    print_warning("Opción inválida")
            except Exception as e:
                print_error(str(e))

            input(Color.paint("\n  Presione Enter para continuar...", Color.BYELLOW))

    # ── Submenú CRUD de permisos ──────────────────────────────────────────────
    def leave_menu(self):
        while True:
            clear()
            print_header("MENÚ PERMISOS")
            print_option("1", "Registrar permiso", Color.BG_GREEN,  Color.BGREEN)
            print_option("2", "Listar permisos",   Color.BG_CYAN,   Color.BCYAN)
            print_option("3", "Eliminar permiso",  Color.BG_RED,    Color.BRED)
            print_option("0", "Volver",            Color.BG_YELLOW, Color.BYELLOW)
            print_separator()

            option = input(Color.paint("  Opción: ", Color.BOLD, Color.BWHITE))

            try:
                if option == "1":
                    clear()
                    self.leave_controller.create()
                elif option == "2":
                    clear()
                    self.leave_controller.read()
                elif option == "3":
                    clear()
                    self.leave_controller.delete()
                elif option == "0":
                    break
                else:
                    print_warning("Opción inválida")
            except Exception as e:
                print_error(str(e))

            input(Color.paint("\n  Presione Enter para continuar...", Color.BYELLOW))

    # ── Vista de estadísticas ─────────────────────────────────────────────────
    def stats_view(self):
        clear()
        StatsController().show()
        input(Color.paint("\n  Presione Enter para continuar...", Color.BYELLOW))

    # ── Menú principal ────────────────────────────────────────────────────────
    def main_menu(self):
        while True:
            clear()
            print_header("SISTEMA DE PERMISOS")
            print_option("1", "Empleados",        Color.BG_GREEN,  Color.BGREEN)
            print_option("2", "Tipos de Permiso", Color.BG_YELLOW, Color.BYELLOW)
            print_option("3", "Permisos",         Color.BG_PURPLE, Color.BMAGENTA)
            print_option("4", "Estadísticas",     Color.BG_CYAN,   Color.BCYAN)
            print_option("0", "Salir",            Color.BG_RED,    Color.BRED)
            print_separator()

            option = input(Color.paint("  Opción: ", Color.BOLD, Color.BWHITE))

            if option == "1":
                self.employee_menu()
            elif option == "2":
                self.leave_type_menu()
            elif option == "3":
                self.leave_menu()
            elif option == "4":
                self.stats_view()
            elif option == "0":
                clear()
                print_header("HASTA LUEGO")
                print(Color.paint("  Saliendo del sistema...".center(55), Color.BOLD, Color.BYELLOW))
                print_separator()
                break
            else:
                print_warning("Opción inválida")
                input(Color.paint("\n  Presione Enter para continuar...", Color.BYELLOW))