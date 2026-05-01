# Controlador de empleados: orquesta el CRUD aplicando validaciones y persistencia.
from core import CrudInterface, JsonManager, LogMixin, ValidationMixin
from models import Employee

class EmployeeController(CrudInterface, ValidationMixin, LogMixin):
    DATA_FILE = "data/employees.json"

    def __init__(self):
        self.db        = JsonManager(EmployeeController.DATA_FILE)
        self.employees = self.db.load()

    def create(self):
        print("\n=== REGISTRAR EMPLEADO ===")
        name   = input("Nombre: ")
        cedula = input("Cédula: ")
        salary = input("Sueldo: ")

        self.validate_not_empty(name,   "Nombre")
        self.validate_not_empty(cedula, "Cédula")
        self.validate_not_empty(salary, "Sueldo")

        employee_id = len(self.employees) + 1
        employee    = Employee(employee_id, name, cedula, float(salary))

        self.employees.append(employee.to_dict())
        self.db.save(self.employees)
        self.log(f"Empleado '{name}' registrado correctamente")

    def read(self):
        print("\n=== EMPLEADOS REGISTRADOS ===")
        if not self.employees:
            print("No hay empleados registrados.")
            return
        for employee_data in self.employees:
            employee = Employee.from_dict(employee_data)
            print(f"{employee.display_name} | Cédula: {employee.cedula} | "
                  f"Sueldo: {employee.salary:.2f} | Valor/hora: {employee.hourly_rate:.4f}")

    def update(self):
        # No requerido según los requisitos funcionales.
        pass

    def delete(self):
        print("\n=== ELIMINAR EMPLEADO ===")
        employee_id = int(input("ID del empleado: "))
        for employee in self.employees:
            if employee["employee_id"] == employee_id:
                self.employees.remove(employee)
                self.db.save(self.employees)
                self.log(f"Empleado con ID {employee_id} eliminado correctamente")
                return
        print("Empleado no encontrado.")
