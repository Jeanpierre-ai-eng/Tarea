# Controlador de permisos: CRUD con validaciones y persistencia.
from core import CrudInterface, JsonManager, LogMixin, ValidationMixin
from models import Employee, LeaveType, Leave


class LeaveController(CrudInterface, ValidationMixin, LogMixin):
    DATA_FILE        = "data/leaves.json"
    EMPLOYEES_FILE   = "data/employees.json"
    LEAVE_TYPES_FILE = "data/leave_types.json"

    def __init__(self):
        self.db          = JsonManager(LeaveController.DATA_FILE)
        self.leaves      = self.db.load()
        self.employees   = JsonManager(LeaveController.EMPLOYEES_FILE).load()
        self.leave_types = JsonManager(LeaveController.LEAVE_TYPES_FILE).load()

    # Muestra la lista de empleados disponibles y retorna el seleccionado.
    def _select_employee(self):
        if not self.employees:
            print("No hay empleados registrados.")
            return None
        print("\n  Empleados disponibles:")
        for e in self.employees:
            employee = Employee.from_dict(e)
            print(f"    {employee.display_name}")
        employee_id = int(input("  ID del empleado: "))
        for e in self.employees:
            if e["employee_id"] == employee_id:
                return e
        print("  Empleado no encontrado.")
        return None

    # Muestra la lista de tipos de permiso disponibles y retorna el seleccionado.
    def _select_leave_type(self):
        if not self.leave_types:
            print("No hay tipos de permiso registrados.")
            return None
        print("\n  Tipos de permiso disponibles:")
        for lt in self.leave_types:
            leave_type = LeaveType.from_dict(lt)
            print(f"    {leave_type.display_name}")
        leave_type_id = int(input("  ID del tipo de permiso: "))
        for lt in self.leave_types:
            if lt["leave_type_id"] == leave_type_id:
                return lt
        print("  Tipo de permiso no encontrado.")
        return None

    def create(self):
        print("\n=== REGISTRAR PERMISO ===")

        employee = self._select_employee()
        if not employee:
            return

        leave_type = self._select_leave_type()
        if not leave_type:
            return

        date_from     = input("  Fecha desde (YYYY-MM-DD): ")
        date_until    = input("  Fecha hasta (YYYY-MM-DD): ")
        duration_type = input("  Modalidad (D=Días / H=Horas): ").upper()

        self.validate_not_empty(date_from,     "Fecha desde")
        self.validate_not_empty(date_until,    "Fecha hasta")
        self.validate_not_empty(duration_type, "Modalidad")

        if duration_type not in (Leave.TYPE_DAYS, Leave.TYPE_HOURS):
            raise ValueError("Modalidad inválida. Use 'D' para días o 'H' para horas.")

        leave_id = len(self.leaves) + 1
        leave    = Leave(leave_id, employee, leave_type, date_from, date_until, duration_type)

        self.leaves.append(leave.to_dict())
        self.db.save(self.leaves)
        self.log(f"Permiso #{leave_id} registrado correctamente")

    def read(self):
        print("\n=== PERMISOS REGISTRADOS ===")
        if not self.leaves:
            print("No hay permisos registrados.")
            return
        for leave_data in self.leaves:
            leave = Leave.from_dict(leave_data)
            print(f"  {leave.summary}")

    def update(self):
        # No requerido según los requisitos funcionales.
        pass

    def delete(self):
        print("\n=== ELIMINAR PERMISO ===")
        leave_id = int(input("ID del permiso: "))
        for leave in self.leaves:
            if leave["leave_id"] == leave_id:
                self.leaves.remove(leave)
                self.db.save(self.leaves)
                self.log(f"Permiso #{leave_id} eliminado correctamente")
                return
        print("Permiso no encontrado.")
