# Controlador de tipos de permiso: CRUD con validaciones y persistencia.
from core import CrudInterface, JsonManager, LogMixin, ValidationMixin
from core import print_header, print_table, print_warning, Color
from models import LeaveType


class LeaveTypeController(CrudInterface, ValidationMixin, LogMixin):
    DATA_FILE = "data/leave_types.json"

    def __init__(self):
        self.db          = JsonManager(LeaveTypeController.DATA_FILE)
        self.leave_types = self.db.load()

    def create(self):
        print_header("REGISTRAR TIPO DE PERMISO", Color.BG_BLUE)
        description = input("  Descripción      : ")
        is_paid     = input("  ¿Remunerado? S/N : ").upper()

        self.validate_not_empty(description, "Descripción")
        self.validate_not_empty(is_paid,     "Remunerado")

        if is_paid not in (LeaveType.PAID, LeaveType.UNPAID):
            raise ValueError("Valor inválido. Use 'S' para remunerado o 'N' para no remunerado.")

        leave_type_id = len(self.leave_types) + 1
        leave_type    = LeaveType(leave_type_id, description, is_paid)

        self.leave_types.append(leave_type.to_dict())
        self.db.save(self.leave_types)
        self.log(f"Tipo de permiso '{description}' registrado correctamente")

    def read(self):
        print_header("TIPOS DE PERMISO REGISTRADOS", Color.BG_BLUE)
        self.leave_types = self.db.load()
        if not self.leave_types:
            print_warning("No hay tipos de permiso registrados.")
            return

        headers = ["ID", "Descripción", "Remunerado"]
        rows    = []
        colors  = {}

        for i, lt in enumerate(self.leave_types):
            leave_type = LeaveType.from_dict(lt)
            if leave_type.affects_salary:
                rem_text  = "✘ No remunerado"
                colors[i] = {2: Color.BRED}
            else:
                rem_text  = "✔ Remunerado"
                colors[i] = {2: Color.BGREEN}
            rows.append([leave_type.leave_type_id, leave_type.description, rem_text])

        # Construye col_colors por columna (no por fila).
        col_colors_map = {}
        for i, row in enumerate(rows):
            for col_idx, color in colors[i].items():
                if col_idx not in col_colors_map:
                    col_colors_map[col_idx] = []
                col_colors_map[col_idx].append((i, color))

        # Impresión manual para soportar color por celda individual.
        from core.console import _table_row, _table_divider, Color as C
        widths = [len(str(h)) for h in headers]
        for row in rows:
            for j, cell in enumerate(row):
                widths[j] = max(widths[j], len(str(cell)))

        _table_row(headers, widths, C.CYAN)
        _table_divider(widths)
        for i, row in enumerate(rows):
            cells = []
            for j, (cell, w) in enumerate(zip(row, widths)):
                cell_color = colors.get(i, {}).get(j, C.WHITE)
                cells.append(C.paint(str(cell).ljust(w), cell_color))
            print(" " + " │ ".join(cells))
        _table_divider(widths, char="─", mid="┴")
        from core.console import Color as Clr
        print(Clr.paint(f"  {len(rows)} registro(s)", Clr.GRAY))

    def update(self):
        # No requerido según los requisitos funcionales.
        pass

    def delete(self):
        print_header("ELIMINAR TIPO DE PERMISO", Color.BG_RED)
        self.leave_types = self.db.load()
        if not self.leave_types:
            print_warning("No hay tipos de permiso registrados.")
            return

        # Muestra tabla resumida para que el usuario identifique el ID.
        headers = ["ID", "Descripción", "Remunerado"]
        rows    = [
            [lt["leave_type_id"], lt["description"], "✔ Sí" if lt["is_paid"] == "S" else "✘ No"]
            for lt in self.leave_types
        ]
        print_table(headers, rows)

        leave_type_id = int(input(Color.paint("  ID a eliminar: ", Color.BOLD, Color.BWHITE)))
        for leave_type in self.leave_types:
            if leave_type["leave_type_id"] == leave_type_id:
                self.leave_types.remove(leave_type)
                self.db.save(self.leave_types)
                self.log(f"Tipo de permiso #{leave_type_id} eliminado correctamente")
                return
        print_warning("Tipo de permiso no encontrado.")
