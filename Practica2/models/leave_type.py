# Modelo de dominio: Producto.
class Product:
    # Atributos estáticos: límites mínimos para validación de dominio.
    MIN_PRICE = 0.01
    MIN_STOCK = 0

    def __init__(self, product_id, name, price, stock):
        # Identificador privado: solo accesible mediante la property `product_id`.
        self._product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    # Property de solo lectura para el ID (atributo encapsulado).
    @property
    def product_id(self):
        return self._product_id

    # Property: indica si el producto tiene unidades disponibles.
    @property
    def is_in_stock(self):
        return self.stock > Product.MIN_STOCK

    # Property: valor total del inventario para este producto.
    @property
    def total_value(self):
        return round(self.price * self.stock, 2)

    # Property: representación legible con stock visible (útil para menús).
    @property
    def display_name(self):
        return f"ID {self.product_id} - {self.name} (stock: {self.stock})"

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }

    # Método estático: factoría desde dict (JSON).
    @staticmethod
    def from_dict(data):
        return Product(
            product_id=data["product_id"],
            name=data["name"],
            price=data["price"],
            stock=data["stock"]
        )

    # Método estático: utilidad de cálculo sin estado.
    @staticmethod
    def calculate_subtotal(price, quantity):
        return round(price * quantity, 2)
