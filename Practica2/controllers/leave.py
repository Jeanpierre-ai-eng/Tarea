# Controlador de productos: CRUD con validaciones y persistencia.
from core import CrudInterface, JsonManager, LogMixin, ValidationMixin
from models import Product


class ProductController(CrudInterface, ValidationMixin, LogMixin):
    DATA_FILE = "data/products.json"

    def __init__(self):
        self.db = JsonManager(ProductController.DATA_FILE)
        self.products = self.db.load()

    def create(self):
        print("\n=== CREAR PRODUCTO ===")

        name = input("Nombre: ")
        price = float(input("Precio: "))
        stock = int(input("Stock: "))

        self.validate_not_empty(name, "Nombre")
        self.validate_positive_number(price, "Precio")
        if price < Product.MIN_PRICE:
            raise ValueError(f"Precio debe ser >= {Product.MIN_PRICE}")
        self.validate_positive_number(stock, "Stock")

        product_id = len(self.products) + 1

        product = Product(product_id, name, price, stock)
        self.products.append(product.to_dict())
        self.db.save(self.products)

        self.log("Producto creado correctamente")

    def read(self):
        print("\n=== PRODUCTOS ===")

        if not self.products:
            print("No hay productos registrados")
            return

        for product_data in self.products:
            product = Product.from_dict(product_data)
            print(product.display_name)

    def update(self):
        print("\n=== ACTUALIZAR PRODUCTO ===")

        product_id = int(input("ID del producto: "))

        for product in self.products:
            if product["product_id"] == product_id:
                product["name"] = input("Nuevo nombre: ")
                product["price"] = float(input("Nuevo precio: "))
                product["stock"] = int(input("Nuevo stock: "))

                self.db.save(self.products)
                self.log("Producto actualizado")
                return

        print("Producto no encontrado")

    def delete(self):
        print("\n=== ELIMINAR PRODUCTO ===")

        product_id = int(input("ID del producto: "))

        for product in self.products:
            if product["product_id"] == product_id:
                self.products.remove(product)
                self.db.save(self.products)
                self.log("Producto eliminado")
                return

        print("Producto no encontrado")
