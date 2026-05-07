from functools import reduce
from datetime import datetime

from core import JsonManager, print_header, print_separator, print_warning, Color
from models import Employee, LeaveType, Leave


class StatsController:
    EMPLOYEES_FILE   = "data/employees.json"
    LEAVE_TYPES_FILE = "data/leave_types.json"
    LEAVES_FILE      = "data/leaves.json"

    def __init__(self):
        self.employees   = JsonManager(StatsController.EMPLOYEES_FILE).load()
        self.leave_types = JsonManager(StatsController.LEAVE_TYPES_FILE).load()
        self.leaves      = JsonManager(StatsController.LEAVES_FILE).load()

    def show(self):
        print_header("ESTADÍSTICAS DE PERMISOS", Color.BG_BLUE)
        self._employee_stats()
        self._leave_type_stats()
        self._leave_stats()

    @staticmethod
    def _row(label, value, val_color=Color.BWHITE):
        lbl = Color.paint(f"  {label:<30}", Color.CYAN)
        val = Color.paint(str(value), val_color)
        print(f"{lbl}: {val}")

    @staticmethod
    def _sub(label, value, val_color=Color.WHITE):
        """Fila secundaria indentada — usada para listas verticales."""
        lbl = Color.paint(f"    {label:<28}", Color.CYAN)
        val = Color.paint(str(value), val_color)
        print(f"{lbl}  {val}")

    def _employee_stats(self):
        print(Color.paint("\n  -- Empleados --", Color.BOLD + Color.BCYAN))
        print_separator()

        if not self.employees:
            print_warning("Sin empleados registrados.")
            return

        total = len(self.employees)

        names = list(map(lambda e: e["name"], self.employees))

        total_salary = reduce(lambda acc, e: acc + e["salary"], self.employees, 0)

        avg_salary = total_salary / total

        highest_paid = reduce(
            lambda a, b: a if a["salary"] >= b["salary"] else b,
            self.employees
        )

        hourly_rates = list(map(
            lambda e: (e["name"], round(e["salary"] / Employee.WORK_HOURS_MONTH, 4)),
            self.employees
        ))

        self._row("Total empleados",         total)
        self._row("Nombres",                 ", ".join(names))
        self._row("Masa salarial total",     f"$ {total_salary:.2f}")
        self._row("Sueldo promedio",         f"$ {avg_salary:.2f}")
        self._row("Mejor remunerado",        f"{highest_paid['name']} ($ {highest_paid['salary']:.2f})", Color.BGREEN)

        print(Color.paint(f"  {'Valor/hora por empleado':<30}:", Color.CYAN))
        for name, rate in hourly_rates:
            self._sub(f"{name}", f"$ {rate:.4f}", Color.BYELLOW)

    def _leave_type_stats(self):
        print(Color.paint("\n  -- Tipos de Permiso --", Color.BOLD + Color.BCYAN))
        print_separator()

        if not self.leave_types:
            print_warning("Sin tipos de permiso registrados.")
            return

        total = len(self.leave_types)

        paid_types   = list(filter(lambda lt: lt["is_paid"] == LeaveType.PAID,   self.leave_types))

        unpaid_types = list(filter(lambda lt: lt["is_paid"] == LeaveType.UNPAID, self.leave_types))

        paid_names   = [lt["description"] for lt in paid_types]
        unpaid_names = [lt["description"] for lt in unpaid_types]

        self._row("Total tipos registrados", total)
        self._row("Remunerados",             len(paid_types),   Color.BGREEN)
        self._row("No remunerados",          len(unpaid_types), Color.BRED)

        if paid_names:
            print(Color.paint(f"  {'Tipos remunerados':<30}:", Color.CYAN))
            for name in paid_names:
                self._sub("✔", name, Color.BGREEN)

        if unpaid_names:
            print(Color.paint(f"  {'Tipos no remunerados':<30}:", Color.CYAN))
            for name in unpaid_names:
                self._sub("✘", name, Color.BRED)

    def _leave_stats(self):
        print(Color.paint("\n  -- Permisos --", Color.BOLD + Color.BCYAN))
        print_separator()

        if not self.leaves:
            print_warning("Sin permisos registrados.")
            return

        total = len(self.leaves)

        paid_leaves = list(filter(
            lambda l: l["leave_type"].get("is_paid") == "S", self.leaves
        ))

        unpaid_leaves = list(filter(
            lambda l: l["leave_type"].get("is_paid") == "N", self.leaves
        ))

        tiempos = list(map(lambda l: l["tiempo"], self.leaves))

        total_tiempo = reduce(lambda acc, t: acc + t, tiempos, 0)

        def calc_deduction(leave):
            hourly_rate = leave["employee"].get("salary", 0) / Employee.WORK_HOURS_MONTH
            hours = leave["tiempo"] * 8 if leave["duration_type"] == Leave.TYPE_DAYS else leave["tiempo"]
            return round(hourly_rate * hours, 2)

        total_deductions = reduce(
            lambda acc, l: acc + calc_deduction(l),
            unpaid_leaves,
            0
        )

        employee_names = {l["employee"]["name"] for l in self.leaves}
        tiempo_by_employee = {
            name: reduce(
                lambda acc, l: acc + (l["tiempo"] if l["employee"]["name"] == name else 0),
                self.leaves,
                0
            )
            for name in employee_names
        }

        top_employee = max(tiempo_by_employee.items(), key=lambda kv: kv[1])

        self._row("Total permisos",           total)
        self._row("Remunerados",              len(paid_leaves),          Color.BGREEN)
        self._row("No remunerados",           len(unpaid_leaves),        Color.BRED)
        self._row("Total tiempo solicitado",  total_tiempo)
        self._row("Total descuentos",         f"$ {total_deductions:.2f}", Color.BRED if total_deductions > 0 else Color.BGREEN)
        self._row("Más permisos",             f"{top_employee[0]} ({top_employee[1]})", Color.BYELLOW)

        print(Color.paint(f"  {'Tiempo por empleado':<30}:", Color.CYAN))
        for name, tiempo in tiempo_by_employee.items():
            self._sub(f"{name}", tiempo, Color.BYELLOW)

        print_separator()
