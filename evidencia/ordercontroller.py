import json

class OrderController:
    FILE = "orders.json"

    def __init__(self):
        try:
            with open(self.FILE, "r") as f:
                self.orders = json.load(f)
        except:
            self.orders = []

    def save(self):
        with open(self.FILE, "w") as f:
            json.dump(self.orders, f, indent=4)

    def create(self):
        customer = input("Cliente: ")
        items = []
        total = 0

        while True:
            name = input("Producto (o 'fin'): ")
            if name == "fin":
                break

            price = float(input("Precio: "))
            qty = int(input("Cantidad: "))

            if price <= 0 or qty <= 0:
                print("Datos inválidos")
                continue

            subtotal = price * qty
            total += subtotal

            items.append({
                "name": name,
                "price": price,
                "quantity": qty,
                "subtotal": subtotal
            })

        order = {
            "id": len(self.orders)+1,
            "customer": customer,
            "items": items,
            "total": total
        }

        self.orders.append(order)
        self.save()
        print("Pedido registrado. Total:", total)

    def read(self):
        for o in self.orders:
            print(o)

    def delete(self):
        id_ = int(input("ID: "))
        self.orders = [o for o in self.orders if o["id"] != id_]
        self.save()
        print("Pedido eliminado")