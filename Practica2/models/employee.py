# Modelo de dominio: Cliente.
class Customer:
    # Atributo estático: longitud esperada de la cédula/RUC.
    IDENTIFICATION_LENGTH = 10

    def __init__(self, customer_id, name, identification):
        # Identificador privado: solo accesible mediante la property `customer_id`.
        self._customer_id = customer_id
        self.name = name
        self.identification = identification

    # Property de solo lectura para el ID (atributo encapsulado).
    @property
    def customer_id(self):
        return self._customer_id

    # Property: representación legible del cliente para listados.
    @property
    def display_name(self):
        return f"ID {self.customer_id} - {self.name}"

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "identification": self.identification
        }

    # Método estático: factoría que reconstruye un Customer desde un dict (JSON).
    @staticmethod
    def from_dict(data):
        return Customer(
            customer_id=data["customer_id"],
            name=data["name"],
            identification=data["identification"]
        )
