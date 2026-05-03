import json

class EquipmentController:
    FILE = "equipment.json"

    def __init__(self):
        try:
            with open(self.FILE, "r") as f:
                self.equipments = json.load(f)
        except:
            self.equipments = []

    def save(self):
        with open(self.FILE, "w") as f:
            json.dump(self.equipments, f, indent=4)

    def create(self):
        name = input("Nombre: ")
        price = float(input("Precio: "))
        stock = int(input("Stock: "))

        if not name:
            print("Nombre obligatorio")
            return
        if price <= 0 or stock < 0:
            print("Datos inválidos")
            return

        equipment = {
            "id": len(self.equipments)+1,
            "name": name,
            "price": price,
            "stock": stock
        }

        self.equipments.append(equipment)
        self.save()
        print("Equipo creado")

    def read(self):
        for e in self.equipments:
            print(e)

    def update(self):
        id_ = int(input("ID: "))
        for e in self.equipments:
            if e["id"] == id_:
                e["name"] = input("Nuevo nombre: ")
                e["price"] = float(input("Nuevo precio: "))
                e["stock"] = int(input("Nuevo stock: "))
                self.save()
                print("Equipo actualizado")
                return
        print("No encontrado")

    def delete(self):
        id_ = int(input("ID: "))
        self.equipments = [e for e in self.equipments if e["id"] != id_]
        self.save()
        print("Equipo eliminado")