# Modelo de dominio: Venta.
class Sale:
    # Atributo estático: tasa de IVA aplicada a todas las ventas.
    IVA_RATE = 0.15

    def __init__(self, sale_id, customer, items, subtotal, iva, total):
        # Identificador privado: solo accesible mediante la property `sale_id`.
        self._sale_id = sale_id
        self.customer = customer
        self.items = items
        self.subtotal = subtotal
        self.iva = iva
        self.total = total

    # Property de solo lectura para el ID (atributo encapsulado).
    @property
    def sale_id(self):
        return self._sale_id

    # Property: nombre del cliente asociado a la venta.
    @property
    def customer_name(self):
        return self.customer.get("name", "—")

    # Property: total de unidades vendidas en esta operación.
    @property
    def item_count(self):
        return sum(item.get("quantity", 0) for item in self.items)

    # Property: resumen legible de la venta.
    @property
    def summary(self):
        return (
            f"Venta #{self.sale_id} - Cliente: {self.customer_name} - "
            f"Items: {self.item_count} - Total: {self.total:.2f}"
        )

    def to_dict(self):
        return {
            "sale_id": self.sale_id,
            "customer": self.customer,
            "items": self.items,
            "subtotal": self.subtotal,
            "iva": self.iva,
            "total": self.total
        }

    # Método estático: cálculo del IVA usando la tasa de la clase.
    @staticmethod
    def calculate_iva(subtotal):
        return round(subtotal * Sale.IVA_RATE, 2)

    # Método estático: factoría desde dict (JSON).
    @staticmethod
    def from_dict(data):
        return Sale(
            sale_id=data["sale_id"],
            customer=data["customer"],
            items=data["items"],
            subtotal=data["subtotal"],
            iva=data["iva"],
            total=data["total"]
        )
