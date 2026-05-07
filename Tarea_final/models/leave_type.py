class LeaveType:
    PAID   = "S"
    UNPAID = "N"

    def __init__(self, leave_type_id, description, is_paid):
        self._leave_type_id = leave_type_id
        self.description = description
        self.is_paid = is_paid  

    @property
    def leave_type_id(self):
        return self._leave_type_id

    @property
    def affects_salary(self):
        return self.is_paid == LeaveType.UNPAID

    @property
    def display_name(self):
        remunerado = "Remunerado" if not self.affects_salary else "No remunerado"
        return f"ID {self.leave_type_id} - {self.description} ({remunerado})"

    def to_dict(self):
        return {
            "leave_type_id": self.leave_type_id,
            "description":   self.description,
            "is_paid":       self.is_paid
        }

    @staticmethod
    def from_dict(data):
        return LeaveType(
            leave_type_id = data["leave_type_id"],
            description   = data["description"],
            is_paid       = data["is_paid"]
        )
