class Leave:
    TYPE_DAYS  = "D"
    TYPE_HOURS = "H"

    def __init__(self, leave_id, employee, leave_type, date_from, date_until, duration_type, tiempo):
        self._leave_id     = leave_id
        self.employee      = employee       
        self.leave_type    = leave_type     
        self.date_from     = date_from      
        self.date_until    = date_until     
        self.duration_type = duration_type  
        self.tiempo        = tiempo         

    @property
    def leave_id(self):
        return self._leave_id

    @property
    def employee_name(self):
        return self.employee.get("name", "—")

    @property
    def leave_type_description(self):
        return self.leave_type.get("description", "—")

    @property
    def affects_salary(self):
        return self.leave_type.get("is_paid") == "N"

    @property
    def summary(self):
        modalidad = "Días"  if self.duration_type == Leave.TYPE_DAYS else "Horas"
        afecta    = "Sí"    if self.affects_salary else "No"
        return (
            f"Permiso #{self.leave_id} - Empleado: {self.employee_name} - "
            f"Tipo: {self.leave_type_description} - "
            f"Desde: {self.date_from} hasta: {self.date_until} - "
            f"Modalidad: {modalidad} - Tiempo: {self.tiempo} - Afecta sueldo: {afecta}"  
        )

    def to_dict(self):
        return {
            "leave_id":      self.leave_id,
            "employee":      self.employee,
            "leave_type":    self.leave_type,
            "date_from":     self.date_from,
            "date_until":    self.date_until,
            "duration_type": self.duration_type,
            "tiempo":        self.tiempo        
        }

    @staticmethod
    def from_dict(data):
        return Leave(
            leave_id      = data["leave_id"],
            employee      = data["employee"],
            leave_type    = data["leave_type"],
            date_from     = data["date_from"],
            date_until    = data["date_until"],
            duration_type = data["duration_type"],
            tiempo        = data["tiempo"]      
        )
