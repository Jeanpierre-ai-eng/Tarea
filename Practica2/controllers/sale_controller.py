# Controlador de ventas: registra ventas y actualiza el inventario.
from core import JsonManager, LogMixin
from models import Sale


class SaleController(LogMixin):
    SALES_FILE = "data/sales.json"
    PRODUCTS_FILE = "data/products.json"
    CUSTOMERS_FILE = "data/customers.json"

    def __init__(self):
        self.sales_db = JsonManager(SaleController.SALES_FILE)
        self.products_db = JsonManager(SaleController.PRODUCTS_FILE)
        self.customers_db = JsonManager(SaleController.CUSTOMERS_FILE)

        self.sales = self.sales_db.load()
        self.products = self.products_db.load()
        self.customers = self.customers_db.load()

    def find_customer(self, customer_id):
        for customer in self.customers:
            if customer["customer_id"] == customer_id:
                return customer
        return None

    def find_product(self, product_id):
        for product in self.products:
            if product["product_id"] == product_id:
                return product
        return None

    def calculate_subtotal(self, items):
        return sum(item["subtotal"] for item in items)

    def register_sale(self, customer, items):
        subtotal = round(self.calculate_subtotal(items), 2)
        iva = Sale.calculate_iva(subtotal)
        total = round(subtotal + iva, 2)

        sale_id = len(self.sales) + 1

        sale = Sale(
            sale_id=sale_id,
            customer=customer,
            items=items,
            subtotal=subtotal,
            iva=iva,
            total=total
        )

        self.sales.append(sale.to_dict())

        self.sales_db.save(self.sales)
        self.products_db.save(self.products)

        self.log("Venta registrada correctamente")
        print(f"Subtotal: {subtotal:.2f}")
        print(f"IVA {int(Sale.IVA_RATE * 100)}%: {iva:.2f}")
        print(f"Total: {total:.2f}")

    def list_sales(self):
        print("\n=== VENTAS ===")

        if not self.sales:
            print("No hay ventas registradas")
            return

        for sale_data in self.sales:
            sale = Sale.from_dict(sale_data)
            print(f"\nVenta #{sale.sale_id} - Cliente: {sale.customer_name}")
            print("  Productos:")
            for item in sale.items:
                print(
                    f"    - {item['name']} x{item['quantity']} "
                    f"@ {item['price']:.2f}  =  {item['subtotal']:.2f}"
                )
            print(
                f"  Subtotal: {sale.subtotal:.2f} | "
                f"IVA: {sale.iva:.2f} | "
                f"Total: {sale.total:.2f}"
            )
