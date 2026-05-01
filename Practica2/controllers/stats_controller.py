# Controlador de estadísticas: consulta general sobre empleados, tipos de permiso y permisos.
# Usa funciones de orden superior (map, filter, reduce) con expresiones lambda
# y list/dict comprehensions sobre los datos persistidos.
from functools import reduce
from datetime import datetime

from core import JsonManager
from models import Employee, LeaveType, Leave


class StatsController:
    EMPLOYEES_FILE   = "data/employees.json"
    LEAVE_TYPES_FILE = "data/leave_types.json"
    LEAVES_FILE      = "data/leaves.json"

    def __init__(self):
        self.employees   = JsonManager(StatsController.EMPLOYEES_FILE).load()
        self.leave_types = JsonManager(StatsController.LEAVE_TYPES_FILE).load()
        self.leaves      = JsonManager(StatsController.LEAVES_FILE).load()

    # Punto de entrada del reporte. Imprime las tres secciones.
    def show(self):
        print("\n=== ESTADÍSTICAS DEL SISTEMA DE PERMISOS ===")
        self._employee_stats()
        self._leave_type_stats()
        self._leave_stats()

    # ---- Empleados ----
    def _employee_stats(self):
        print("\n-- Empleados --")

        if not self.employees:
            print("  Sin empleados registrados.")
            return

        total = len(self.employees)

        # map + lambda: extrae los nombres de todos los empleados.
        names = list(map(lambda e: e["name"], self.employees))

        # reduce + lambda: suma total de sueldos.
        total_salary = reduce(lambda acc, e: acc + e["salary"], self.employees, 0)

        # reduce + lambda: sueldo promedio.
        avg_salary = total_salary / total

        # reduce + lambda: empleado con mayor sueldo.
        highest_paid = reduce(
            lambda a, b: a if a["salary"] >= b["salary"] else b,
            self.employees
        )

        # map + lambda: calcula el valor/hora de cada empleado.
        hourly_rates = list(map(
            lambda e: (e["name"], round(e["salary"] / Employee.WORK_HOURS_MONTH, 4)),
            self.employees
        ))

        print(f"  Total empleados registrados : {total}")
        print(f"  Nombres                     : {', '.join(names)}")
        print(f"  Masa salarial total         : {total_salary:.2f}")
        print(f"  Sueldo promedio             : {avg_salary:.2f}")
        print(f"  Empleado mejor remunerado   : {highest_paid['name']} ({highest_paid['salary']:.2f})")
        print(f"  Valor/hora por empleado     : {hourly_rates}")

    # ---- Tipos de permiso ----
    def _leave_type_stats(self):
        print("\n-- Tipos de Permiso --")

        if not self.leave_types:
            print("  Sin tipos de permiso registrados.")
            return

        total = len(self.leave_types)

        # filter + lambda: tipos remunerados (is_paid == "S").
        paid_types = list(filter(lambda lt: lt["is_paid"] == LeaveType.PAID, self.leave_types))

        # filter + lambda: tipos no remunerados (is_paid == "N").
        unpaid_types = list(filter(lambda lt: lt["is_paid"] == LeaveType.UNPAID, self.leave_types))

        # comprehension: nombres de tipos remunerados.
        paid_names   = [lt["description"] for lt in paid_types]

        # comprehension: nombres de tipos no remunerados.
        unpaid_names = [lt["description"] for lt in unpaid_types]

        print(f"  Total tipos registrados : {total}")
        print(f"  Remunerados             : {len(paid_types)}  → {', '.join(paid_names)   if paid_names   else '—'}")
        print(f"  No remunerados          : {len(unpaid_types)} → {', '.join(unpaid_names) if unpaid_names else '—'}")

    # ---- Permisos ----
    def _leave_stats(self):
        print("\n-- Permisos --")

        if not self.leaves:
            print("  Sin permisos registrados.")
            return

        total = len(self.leaves)

        # filter + lambda: permisos remunerados (is_paid == "S").
        paid_leaves = list(filter(
            lambda l: l["leave_type"].get("is_paid") == "S",
            self.leaves
        ))

        # filter + lambda: permisos no remunerados (is_paid == "N").
        unpaid_leaves = list(filter(
            lambda l: l["leave_type"].get("is_paid") == "N",
            self.leaves
        ))

        # --- Total tiempo solicitado ---
        # Función auxiliar: calcula días entre fecha_desde y fecha_hasta.
        def days_between(leave):
            fmt        = "%Y-%m-%d"
            date_from  = datetime.strptime(leave["date_from"],  fmt)
            date_until = datetime.strptime(leave["date_until"], fmt)
            return (date_until - date_from).days + 1

        # map + lambda: días por cada permiso.
        days_per_leave = list(map(lambda l: days_between(l), self.leaves))

        # reduce + lambda: total de días solicitados.
        total_days = reduce(lambda acc, d: acc + d, days_per_leave, 0)

        # --- Total descuentos ---
        # map + lambda: calcula el descuento de cada permiso no remunerado.
        def calc_deduction(leave):
            hourly_rate = leave["employee"].get("salary", 0) / Employee.WORK_HOURS_MONTH
            days        = days_between(leave)
            hours       = days * 8  # jornada laboral estándar: 8 horas/día
            return round(hourly_rate * hours, 2)

        # reduce sobre permisos no remunerados: suma total de descuentos.
        total_deductions = reduce(
            lambda acc, l: acc + calc_deduction(l),
            unpaid_leaves,
            0
        )

        # dict comprehension: total de días de permiso por empleado.
        employee_names = {l["employee"]["name"] for l in self.leaves}
        days_by_employee = {
            name: reduce(
                lambda acc, l: acc + (days_between(l) if l["employee"]["name"] == name else 0),
                self.leaves,
                0
            )
            for name in employee_names
        }

        # max con lambda: empleado con más días de permiso.
        top_employee = max(days_by_employee.items(), key=lambda kv: kv[1])

        print(f"  Total permisos registrados  : {total}")
        print(f"  Permisos remunerados        : {len(paid_leaves)}")
        print(f"  Permisos no remunerados     : {len(unpaid_leaves)}")
        print(f"  Total días solicitados      : {total_days} día(s)")
        print(f"  Total descuentos generados  : {total_deductions:.2f}")
        print(f"  Días por empleado           : {days_by_employee}")
        print(f"  Empleado con más permisos   : {top_employee[0]} ({top_employee[1]} día(s))")
