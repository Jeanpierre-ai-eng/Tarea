class Employee:
    WORK_HOURS_MONTH = 240

    def __init__(self, employee_id, name, cedula, salary):
        self._employee_id = employee_id
        self.name = name
        self.cedula = cedula
        self.salary = salary

    @property
    def employee_id(self):
        return self._employee_id

    @property
    def hourly_rate(self):
        return round(self.salary / Employee.WORK_HOURS_MONTH, 4)

    @property
    def display_name(self):
        return f"ID {self.employee_id} - {self.name}"

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "name":        self.name,
            "cedula":      self.cedula,
            "salary":      self.salary
        }

    @staticmethod
    def from_dict(data):
        return Employee(
            employee_id = data["employee_id"],
            name        = data["name"],
            cedula      = data["cedula"],
            salary      = data["salary"]
        )
