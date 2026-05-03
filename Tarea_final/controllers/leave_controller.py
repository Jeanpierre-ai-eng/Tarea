# Controlador de permisos: CRUD con validaciones y persistencia.
from core import CrudInterface, JsonManager, LogMixin, ValidationMixin
from core import print_header, print_separator, print_warning, print_table, Color
from core.console import _table_row, _table_divider
from models import Employee, LeaveType, Leave


class LeaveController(CrudInterface, ValidationMixin, LogMixin):
    DATA_FILE        = "data/leaves.json"
    EMPLOYEES_FILE   = "data/employees.json"
    LEAVE_TYPES_FILE = "data/leave_types.json"

    def __init__(self):
        self.db          = JsonManager(LeaveController.DATA_FILE)
        self.leaves      = self.db.load()
        self.employees   = []
        self.leave_types = []

    # Muestra la lista de empleados disponibles y retorna el seleccionado.
    # Recarga el JSON en cada llamada para reflejar registros nuevos en la sesión.
    def _select_employee(self):
        self.employees = JsonManager(LeaveController.EMPLOYEES_FILE).load()
        if not self.employees:
            print_warning("No hay empleados registrados.")
            return None
        print(Color.paint("\n  Empleados disponibles:", Color.CYAN))
        for e in self.employees:
            employee = Employee.from_dict(e)
            print(Color.paint(f"    {employee.display_name}", Color.WHITE))
        employee_id = int(input(Color.paint("  ID del empleado: ", Color.BWHITE)))
        for e in self.employees:
            if e["employee_id"] == employee_id:
                return e
        print_warning("Empleado no encontrado.")
        return None

    # Muestra la lista de tipos de permiso disponibles y retorna el seleccionado.
    # Recarga el JSON en cada llamada para reflejar registros nuevos en la sesión.
    def _select_leave_type(self):
        self.leave_types = JsonManager(LeaveController.LEAVE_TYPES_FILE).load()
        if not self.leave_types:
            print_warning("No hay tipos de permiso registrados.")
            return None
        print(Color.paint("\n  Tipos de permiso disponibles:", Color.CYAN))
        for lt in self.leave_types:
            leave_type = LeaveType.from_dict(lt)
            print(Color.paint(f"    {leave_type.display_name}", Color.WHITE))
        leave_type_id = int(input(Color.paint("  ID del tipo de permiso: ", Color.BWHITE)))
        for lt in self.leave_types:
            if lt["leave_type_id"] == leave_type_id:
                return lt
        print_warning("Tipo de permiso no encontrado.")
        return None

    # Calcula el descuento según modalidad y tipo de permiso.
    def _calc_deduction(self, employee, leave_type, tiempo, duration_type):
        if leave_type.get("is_paid") == LeaveType.PAID:
            return 0.0
        hourly_rate = employee.get("salary", 0) / Employee.WORK_HOURS_MONTH
        hours = tiempo * 8 if duration_type == Leave.TYPE_DAYS else tiempo
        return round(hourly_rate * hours, 2)

    # Imprime el resumen del permiso antes de confirmar.
    def _print_summary(self, employee, leave_type, date_from, date_until, duration_type, tiempo, deduction):
        remunerado     = "Sí"    if leave_type.get("is_paid") == LeaveType.PAID else "No"
        modalidad      = "Días"  if duration_type == Leave.TYPE_DAYS else "Horas"
        rem_color      = Color.BGREEN if remunerado == "Sí" else Color.BRED
        desc_color     = Color.BGREEN if deduction == 0.0   else Color.BRED
        print_separator()
        print(Color.paint("  Resumen:", Color.BOLD + Color.BWHITE))
        print(Color.paint(f"    {'Empleado':<20}: ", Color.CYAN) + Color.paint(employee.get('name'), Color.WHITE))
        print(Color.paint(f"    {'Tipo de permiso':<20}: ", Color.CYAN) + Color.paint(leave_type.get('description'), Color.WHITE))
        print(Color.paint(f"    {'Desde':<20}: ", Color.CYAN) + Color.paint(f"{date_from}  →  {date_until}", Color.WHITE))
        print(Color.paint(f"    {'Modalidad':<20}: ", Color.CYAN) + Color.paint(f"{modalidad}  |  Tiempo: {tiempo}", Color.WHITE))
        print(Color.paint(f"    {'¿Remunerado?':<20}: ", Color.CYAN) + Color.paint(remunerado, rem_color))
        print(Color.paint(f"    {'Descuento':<20}: ", Color.CYAN) + Color.paint(f"$ {deduction:.2f}", desc_color))
        print_separator()

    def create(self):
        print_header("REGISTRAR PERMISO", Color.BG_PURPLE)

        employee = self._select_employee()
        if not employee:
            return

        leave_type = self._select_leave_type()
        if not leave_type:
            return

        date_from     = input(Color.paint("  Fecha desde (YYYY-MM-DD): ", Color.BWHITE))
        date_until    = input(Color.paint("  Fecha hasta (YYYY-MM-DD): ", Color.BWHITE))
        duration_type = input(Color.paint("  Modalidad (D=Días / H=Horas): ", Color.BWHITE)).upper()
        tiempo        = input(Color.paint("  Tiempo (cantidad): ", Color.BWHITE))

        self.validate_not_empty(date_from,     "Fecha desde")
        self.validate_not_empty(date_until,    "Fecha hasta")
        self.validate_not_empty(duration_type, "Modalidad")
        self.validate_not_empty(tiempo,        "Tiempo")
        self.validate_date(date_from,          "Fecha desde")
        self.validate_date(date_until,         "Fecha hasta")
        self.validate_duration_type(duration_type)
        self.validate_positive_number(float(tiempo), "Tiempo")

        tiempo_float = float(tiempo)
        deduction    = self._calc_deduction(employee, leave_type, tiempo_float, duration_type)
        self._print_summary(employee, leave_type, date_from, date_until, duration_type, tiempo_float, deduction)

        # Confirmación numérica antes de persistir.
        print(Color.paint("  1", Color.WHITE, Color.BG_GREEN) + Color.paint(" Confirmar   ", Color.BGREEN) +
              Color.paint("  2", Color.WHITE, Color.BG_RED)   + Color.paint(" Cancelar",    Color.BRED))
        opcion = input(Color.paint("\n  Opción: ", Color.BOLD, Color.BWHITE)).strip()
        if opcion != "1":
            print_warning("Operación cancelada.")
            return

        self.leaves  = self.db.load()
        leave_id     = len(self.leaves) + 1
        leave        = Leave(leave_id, employee, leave_type, date_from, date_until, duration_type, tiempo_float)

        self.leaves.append(leave.to_dict())
        self.db.save(self.leaves)
        self.log(f"Permiso #{leave_id} registrado correctamente")

    def read(self):
        print_header("PERMISOS REGISTRADOS", Color.BG_PURPLE)
        self.leaves = self.db.load()
        if not self.leaves:
            print_warning("No hay permisos registrados.")
            return

        headers = ["ID", "Empleado", "Tipo", "Desde", "Hasta", "Mod", "Tiempo", "Descuento"]
        rows    = []
        row_colors = []

        for ld in self.leaves:
            leave      = Leave.from_dict(ld)
            deduction  = self._calc_deduction(ld["employee"], ld["leave_type"], ld["tiempo"], ld["duration_type"])
            desc_color = Color.BGREEN if deduction == 0.0 else Color.BRED
            rows.append([
                leave.leave_id,
                leave.employee_name,
                leave.leave_type_description,
                leave.date_from,
                leave.date_until,
                leave.duration_type,
                leave.tiempo,
                f"$ {deduction:.2f}"
            ])
            row_colors.append({7: desc_color})

        # Calcula anchos.
        widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))

        _table_row(headers, widths, Color.CYAN)
        _table_divider(widths)
        for i, row in enumerate(rows):
            cells = []
            for j, (cell, w) in enumerate(zip(row, widths)):
                cell_color = row_colors[i].get(j, Color.WHITE)
                cells.append(Color.paint(str(cell).ljust(w), cell_color))
            print(" " + " │ ".join(cells))
        _table_divider(widths, char="─", mid="┴")
        print(Color.paint(f"  {len(rows)} permiso(s) registrado(s)", Color.GRAY))

    def update(self):
        # No requerido según los requisitos funcionales.
        pass

    def delete(self):
        print_header("ELIMINAR PERMISO", Color.BG_RED)
        self.leaves = self.db.load()
        if not self.leaves:
            print_warning("No hay permisos registrados.")
            return

        # Muestra tabla resumida para que el usuario identifique el ID.
        headers = ["ID", "Empleado", "Tipo", "Desde", "Hasta"]
        rows    = [
            [
                l["leave_id"],
                l["employee"]["name"],
                l["leave_type"]["description"],
                l["date_from"],
                l["date_until"]
            ]
            for l in self.leaves
        ]
        print_table(headers, rows)

        leave_id = int(input(Color.paint("  ID a eliminar: ", Color.BOLD, Color.BWHITE)))
        for leave in self.leaves:
            if leave["leave_id"] == leave_id:
                self.leaves.remove(leave)
                self.db.save(self.leaves)
                self.log(f"Permiso #{leave_id} eliminado correctamente")
                return
        print_warning("Permiso no encontrado.")