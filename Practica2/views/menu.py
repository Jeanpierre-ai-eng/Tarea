from controllers import (
    CustomerController,
    ProductController,
    SaleController,
    StatsController,
)
from core import ask_continue
from models import Customer, Product


# Capa de presentación: muestra menús por consola y delega las operaciones
# en los controladores correspondientes (clientes, productos y ventas).
class Menu:
    def __init__(self):
        # Instancias de los controladores que encapsulan la lógica de negocio.
        self.customer_controller = CustomerController()
        self.product_controller = ProductController()
        self.sale_controller = SaleController()

    # Submenú CRUD de clientes.
    def customer_menu(self):
        while True:
            print("\n=== MENÚ CLIENTES ===")
            print("1. Crear cliente")
            print("2. Listar clientes")
            print("3. Actualizar cliente")
            print("4. Eliminar cliente")
            print("0. Volver")

            option = input("Opción: ")

            try:
                if option == "1":
                    self.customer_controller.create()
                elif option == "2":
                    self.customer_controller.read()
                elif option == "3":
                    self.customer_controller.update()
                elif option == "4":
                    self.customer_controller.delete()
                elif option == "0":
                    break
                else:
                    print("Opción inválida")
            except Exception as e:
                print("Error:", e)

    # Submenú CRUD de productos.
    def product_menu(self):
        while True:
            print("\n=== MENÚ PRODUCTOS ===")
            print("1. Crear producto")
            print("2. Listar productos")
            print("3. Actualizar producto")
            print("4. Eliminar producto")
            print("0. Volver")

            option = input("Opción: ")

            try:
                if option == "1":
                    self.product_controller.create()
                elif option == "2":
                    self.product_controller.read()
                elif option == "3":
                    self.product_controller.update()
                elif option == "4":
                    self.product_controller.delete()
                elif option == "0":
                    break
                else:
                    print("Opción inválida")
            except Exception as e:
                print("Error:", e)

    # Submenú de ventas: registro y listado.
    def sale_menu(self):
        while True:
            print("\n=== MENÚ VENTAS ===")
            print("1. Crear venta")
            print("2. Listar ventas")
            print("0. Volver")

            option = input("Opción: ")

            try:
                if option == "1":
                    self._create_sale_flow()
                elif option == "2":
                    SaleController().list_sales()
                elif option == "0":
                    break
                else:
                    print("Opción inválida")
            except Exception as e:
                print("Error:", e)

    # Flujo interactivo de creación de venta. Muestra los listados de clientes
    # y productos antes de solicitar los IDs y delega la persistencia al controlador.
    def _create_sale_flow(self):
        sale_controller = SaleController()

        print("\n=== CREAR VENTA ===")

        customer = self._select_customer(sale_controller)
        if customer is None:
            return

        items = self._select_items(sale_controller)
        if not items:
            return

        sale_controller.register_sale(customer, items)

    # Lista los clientes disponibles y solicita la selección por ID.
    def _select_customer(self, sale_controller):
        if not sale_controller.customers:
            print("No hay clientes registrados")
            return None

        print("\n--- Clientes disponibles ---")
        for c_data in sale_controller.customers:
            print(f"  {Customer.from_dict(c_data).display_name}")

        customer_id = int(input("\nID del cliente: "))
        customer = sale_controller.find_customer(customer_id)

        if not customer:
            print("Cliente no encontrado")
            return None

        return customer

    # Lista los productos disponibles (con stock) y arma la lista de ítems.
    # El decorador ask_continue repite la captura mientras el usuario confirme.
    def _select_items(self, sale_controller):
        if not sale_controller.products:
            print("No hay productos registrados")
            return []

        @ask_continue("¿Desea agregar otro producto a la venta? (s/n): ")
        def add_one_item():
            print("\n--- Productos disponibles ---")
            for p_data in sale_controller.products:
                print(f"  {Product.from_dict(p_data).display_name}")

            product_id = int(input("\nID del producto: "))
            product = sale_controller.find_product(product_id)

            if not product:
                print("Producto no encontrado")
                return None

            quantity = int(input("Cantidad: "))
            if quantity > product["stock"]:
                print("Stock insuficiente")
                return None

            product["stock"] -= quantity
            return {
                "product_id": product["product_id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "subtotal": Product.calculate_subtotal(product["price"], quantity)
            }

        return add_one_item()

    # Vista de consulta general: delega en StatsController y muestra estadísticas
    # calculadas con map / filter / reduce + lambdas y comprehensions.
    def stats_view(self):
        StatsController().show()

    # Menú principal: punto de entrada que dirige hacia los submenús.
    def main_menu(self):
        while True:
            print("\n==============================")
            print(" SISTEMA DE VENTAS CON JSON ")
            print("==============================")
            print("1. Clientes")
            print("2. Productos")
            print("3. Ventas")
            print("4. Consulta general / Estadísticas")
            print("0. Salir")

            option = input("Opción: ")

            if option == "1":
                self.customer_menu()
            elif option == "2":
                self.product_menu()
            elif option == "3":
                self.sale_menu()
            elif option == "4":
                self.stats_view()
            elif option == "0":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida")
