import json

class Supplier:
    def __init__(self, supplier_id, name, identification):
        self.supplier_id = supplier_id
        self.name = name
        self.identification = identification

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Supplier(**data)


class SupplierController:
    FILE = "suppliers.json"

    def __init__(self):
        try:
            with open(self.FILE, "r") as f:
                self.suppliers = json.load(f)
        except:
            self.suppliers = []

    def save(self):
        with open(self.FILE, "w") as f:
            json.dump(self.suppliers, f, indent=4)

    def create(self):
        name = input("Nombre proveedor: ")
        identification = input("Identificación: ")

        if not name or not identification:
            print("Campos obligatorios")
            return

        supplier = Supplier(len(self.suppliers)+1, name, identification)
        self.suppliers.append(supplier.to_dict())
        self.save()
        print("Proveedor creado")

    def read(self):
        for s in self.suppliers:
            print(s)

    def update(self):
        supplier_id = int(input("ID: "))
        for s in self.suppliers:
            if s["supplier_id"] == supplier_id:
                s["name"] = input("Nuevo nombre: ")
                s["identification"] = input("Nueva identificación: ")
                self.save()
                print("Proveedor actualizado")
                return
        print("No encontrado")

    def delete(self):
        supplier_id = int(input("ID: "))
        self.suppliers = [s for s in self.suppliers if s["supplier_id"] != supplier_id]
        self.save()
        print("Proveedor eliminado")