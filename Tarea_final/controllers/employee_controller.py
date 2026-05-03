# Controlador de empleados: orquesta el CRUD aplicando validaciones y persistencia.
from core import CrudInterface, JsonManager, LogMixin, ValidationMixin
from core import print_header, print_table, print_warning, print_error, Color
from models import Employee


class EmployeeController(CrudInterface, ValidationMixin, LogMixin):
    DATA_FILE = "data/employees.json"

    def __init__(self):
        self.db        = JsonManager(EmployeeController.DATA_FILE)
        self.employees = self.db.load()

    def create(self):
        print_header("REGISTRAR EMPLEADO", Color.BG_PURPLE)

        # Nombre: solo letras y espacios, con reintento en bucle.
        while True:
            name = input(Color.paint("  Nombre : ", Color.BWHITE))
            try:
                self.validate_not_empty(name, "Nombre")
                self.validate_only_letters(name, "Nombre")
                break
            except ValueError as e:
                print_error(str(e))

        # Cédula: validación módulo 10, con reintento en bucle.
        while True:
            cedula = input(Color.paint("  Cédula : ", Color.BWHITE))
            try:
                self.validate_not_empty(cedula, "Cédula")
                self.validate_cedula_ecuatoriana(cedula)
                break
            except ValueError as e:
                print_error(str(e))

        # Sueldo: solo número positivo, con reintento en bucle.
        while True:
            salary = input(Color.paint("  Sueldo : ", Color.BWHITE))
            try:
                self.validate_not_empty(salary, "Sueldo")
                self.validate_numeric(salary, "Sueldo")
                self.validate_positive_number(float(salary), "Sueldo")
                break
            except ValueError as e:
                print_error(str(e))

        employee_id = len(self.employees) + 1
        employee    = Employee(employee_id, name, cedula, float(salary))

        self.employees.append(employee.to_dict())
        self.db.save(self.employees)
        self.log(f"Empleado '{name}' registrado correctamente")

    def read(self):
        print_header("EMPLEADOS REGISTRADOS", Color.BG_PURPLE)
        # Recarga para mostrar siempre el estado actual del JSON.
        self.employees = self.db.load()
        if not self.employees:
            print_warning("No hay empleados registrados.")
            return

        headers = ["ID", "Nombre", "Cédula", "Sueldo", "Val/hora"]
        rows    = []
        for e in self.employees:
            emp = Employee.from_dict(e)
            rows.append([
                emp.employee_id,
                emp.name,
                emp.cedula,
                f"$ {emp.salary:.2f}",
                f"{emp.hourly_rate:.4f}"
            ])

        print_table(headers, rows)

    def update(self):
        # No requerido según los requisitos funcionales.
        pass

    def delete(self):
        print_header("ELIMINAR EMPLEADO", Color.BG_RED)
        self.employees = self.db.load()
        if not self.employees:
            print_warning("No hay empleados registrados.")
            return

        # Muestra tabla resumida para que el usuario identifique el ID.
        headers = ["ID", "Nombre", "Cédula"]
        rows    = [[e["employee_id"], e["name"], e["cedula"]] for e in self.employees]
        print_table(headers, rows)

        employee_id = int(input(Color.paint("  ID a eliminar: ", Color.BOLD, Color.BWHITE)))
        for employee in self.employees:
            if employee["employee_id"] == employee_id:
                self.employees.remove(employee)
                self.db.save(self.employees)
                self.log(f"Empleado con ID {employee_id} eliminado correctamente")
                return
        print_warning("Empleado no encontrado.")
