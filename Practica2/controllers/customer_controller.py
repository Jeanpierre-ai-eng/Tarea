# Controlador de clientes: orquesta el CRUD aplicando validaciones y persistencia.
from core import CrudInterface, JsonManager, LogMixin, ValidationMixin
from models import Customer


class CustomerController(CrudInterface, ValidationMixin, LogMixin):
    DATA_FILE = "data/customers.json"

    def __init__(self):
        self.db = JsonManager(CustomerController.DATA_FILE)
        self.customers = self.db.load()

    def create(self):
        print("\n=== CREAR CLIENTE ===")

        name = input("Nombre: ")
        identification = input("Cédula/RUC: ")

        self.validate_not_empty(name, "Nombre")
        self.validate_not_empty(identification, "Cédula/RUC")

        customer_id = len(self.customers) + 1

        customer = Customer(customer_id, name, identification)
        self.customers.append(customer.to_dict())
        self.db.save(self.customers)

        self.log("Cliente creado correctamente")

    def read(self):
        print("\n=== CLIENTES ===")

        if not self.customers:
            print("No hay clientes registrados")
            return

        for customer_data in self.customers:
            customer = Customer.from_dict(customer_data)
            print(customer.display_name)

    def update(self):
        print("\n=== ACTUALIZAR CLIENTE ===")

        customer_id = int(input("ID del cliente: "))

        for customer in self.customers:
            if customer["customer_id"] == customer_id:
                customer["name"] = input("Nuevo nombre: ")
                customer["identification"] = input("Nueva cédula/RUC: ")

                self.db.save(self.customers)
                self.log("Cliente actualizado")
                return

        print("Cliente no encontrado")

    def delete(self):
        print("\n=== ELIMINAR CLIENTE ===")

        customer_id = int(input("ID del cliente: "))

        for customer in self.customers:
            if customer["customer_id"] == customer_id:
                self.customers.remove(customer)
                self.db.save(self.customers)
                self.log("Cliente eliminado")
                return

        print("Cliente no encontrado")
