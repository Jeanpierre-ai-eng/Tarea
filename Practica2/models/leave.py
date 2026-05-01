# Modelo de dominio: Permiso.
class Leave:
    # Atributos estáticos: modalidades de duración del permiso.
    TYPE_DAYS  = "D"
    TYPE_HOURS = "H"

    def __init__(self, leave_id, employee, leave_type, date_from, date_until, duration_type):
        # Identificador privado: solo accesible mediante la property `leave_id`.
        self._leave_id = leave_id
        self.employee      = employee       # dict con datos del empleado
        self.leave_type    = leave_type     # dict con datos del tipo de permiso
        self.date_from     = date_from      # string "YYYY-MM-DD"
        self.date_until    = date_until     # string "YYYY-MM-DD"
        self.duration_type = duration_type  # "D" = días completos | "H" = horas

    # Property de solo lectura para el ID (atributo encapsulado).
    @property
    def leave_id(self):
        return self._leave_id

    # Property: nombre del empleado asociado al permiso.
    @property
    def employee_name(self):
        return self.employee.get("name", "—")

    # Property: descripción del tipo de permiso.
    @property
    def leave_type_description(self):
        return self.leave_type.get("description", "—")

    # Property: indica si este permiso descuenta del sueldo.
    # Compara contra "N" directamente para evitar dependencia con la clase LeaveType.
    @property
    def affects_salary(self):
        return self.leave_type.get("is_paid") == "N"

    # Property: resumen legible del permiso.
    @property
    def summary(self):
        modalidad = "Días"  if self.duration_type == Leave.TYPE_DAYS else "Horas"
        afecta    = "Sí"    if self.affects_salary else "No"
        return (
            f"Permiso #{self.leave_id} - Empleado: {self.employee_name} - "
            f"Tipo: {self.leave_type_description} - "
            f"Desde: {self.date_from} hasta: {self.date_until} - "
            f"Modalidad: {modalidad} - Afecta sueldo: {afecta}"
        )

    def to_dict(self):
        return {
            "leave_id":      self.leave_id,
            "employee":      self.employee,
            "leave_type":    self.leave_type,
            "date_from":     self.date_from,
            "date_until":    self.date_until,
            "duration_type": self.duration_type
        }

    @staticmethod
    def from_dict(data):
        return Leave(
            leave_id      = data["leave_id"],
            employee      = data["employee"],
            leave_type    = data["leave_type"],
            date_from     = data["date_from"],
            date_until    = data["date_until"],
            duration_type = data["duration_type"]
        )
