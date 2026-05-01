# Controlador de tipos de permiso: CRUD con validaciones y persistencia.
from core import CrudInterface, JsonManager, LogMixin, ValidationMixin
from models import LeaveType

class LeaveTypeController(CrudInterface, ValidationMixin, LogMixin):
    DATA_FILE = "data/leave_types.json"

    def __init__(self):
        self.db = JsonManager(LeaveTypeController.DATA_FILE)

    # Recarga los datos desde el archivo JSON en cada operación.
    def _reload(self):
        self.leave_types = self.db.load()

    def create(self):
        self._reload()
        print("\n=== REGISTRAR TIPO DE PERMISO ===")
        description = input("Descripción: ")
        is_paid     = input("¿Es remunerado? (S/N): ").upper()

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
        self._reload()
        print("\n=== TIPOS DE PERMISO REGISTRADOS ===")
        if not self.leave_types:
            print("No hay tipos de permiso registrados.")
            return
        for leave_type_data in self.leave_types:
            leave_type = LeaveType.from_dict(leave_type_data)
            print(f"  {leave_type.display_name}")

    def update(self):
        # No requerido según los requisitos funcionales.
        pass

    def delete(self):
        self._reload()
        print("\n=== ELIMINAR TIPO DE PERMISO ===")
        leave_type_id = int(input("ID del tipo de permiso: "))
        for leave_type in self.leave_types:
            if leave_type["leave_type_id"] == leave_type_id:
                self.leave_types.remove(leave_type)
                self.db.save(self.leave_types)
                self.log(f"Tipo de permiso #{leave_type_id} eliminado correctamente")
                return
        print("Tipo de permiso no encontrado.")
