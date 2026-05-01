# Controlador de estadísticas: consulta general sobre clientes, productos y ventas.
# Demuestra el uso de funciones de orden superior (map, filter, reduce) con
# expresiones lambda y list/dict comprehensions sobre los datos persistidos.
from functools import reduce

from core import JsonManager
from models import Customer


class StatsController:
    CUSTOMERS_FILE = "data/customers.json"
    PRODUCTS_FILE = "data/products.json"
    SALES_FILE = "data/sales.json"

    def __init__(self):
        self.customers = JsonManager(StatsController.CUSTOMERS_FILE).load()
        self.products = JsonManager(StatsController.PRODUCTS_FILE).load()
        self.sales = JsonManager(StatsController.SALES_FILE).load()

    # Punto de entrada del reporte. Imprime las tres secciones.
    def show(self):
        print("\n=== CONSULTA GENERAL / ESTADÍSTICAS ===")
        self._customer_stats()
        self._product_stats()
        self._sale_stats()

    # ---- Clientes ----
    def _customer_stats(self):
        print("\n-- Clientes --")

        if not self.customers:
            print("  Sin clientes registrados")
            return

        # map + lambda: extrae los nombres.
        names = list(map(lambda c: c["name"], self.customers))

        # filter + lambda: clientes con identificación de longitud válida.
        valid = list(filter(
            lambda c: len(c["identification"]) == Customer.IDENTIFICATION_LENGTH,
            self.customers
        ))

        # comprehension: clientes con identificación inválida.
        invalid_ids = [
            c["identification"]
            for c in self.customers
            if len(c["identification"]) != Customer.IDENTIFICATION_LENGTH
        ]

        print(f"  Total registrados: {len(self.customers)}")
        print(f"  Nombres: {', '.join(names)}")
        print(f"  Con identificación válida ({Customer.IDENTIFICATION_LENGTH} dígitos): {len(valid)}")
        print(f"  Identificaciones inválidas: {invalid_ids if invalid_ids else '—'}")

    # ---- Productos ----
    def _product_stats(self):
        print("\n-- Productos --")

        if not self.products:
            print("  Sin productos registrados")
            return

        total = len(self.products)

        # reduce + lambda: valor total del inventario (Σ price * stock).
        inventory_value = reduce(
            lambda acc, p: acc + p["price"] * p["stock"],
            self.products,
            0
        )

        # reduce + lambda: precio promedio.
        avg_price = reduce(lambda acc, p: acc + p["price"], self.products, 0) / total

        # reduce + lambda: producto más caro.
        most_expensive = reduce(
            lambda a, b: a if a["price"] >= b["price"] else b,
            self.products
        )

        # filter + lambda: productos sin stock.
        out_of_stock = list(filter(lambda p: p["stock"] == 0, self.products))

        # comprehension: nombres de productos disponibles.
        in_stock_names = [p["name"] for p in self.products if p["stock"] > 0]

        # map + lambda: pares (nombre, valor en inventario).
        valuations = list(map(
            lambda p: (p["name"], round(p["price"] * p["stock"], 2)),
            self.products
        ))

        print(f"  Total registrados: {total}")
        print(f"  Valor total del inventario: {inventory_value:.2f}")
        print(f"  Precio promedio: {avg_price:.2f}")
        print(f"  Producto más caro: {most_expensive['name']} ({most_expensive['price']:.2f})")
        print(f"  Productos sin stock: {len(out_of_stock)}")
        print(f"  Productos con stock disponible: {', '.join(in_stock_names) if in_stock_names else '—'}")
        print(f"  Valor por producto: {valuations}")

    # ---- Ventas ----
    def _sale_stats(self):
        print("\n-- Ventas --")

        if not self.sales:
            print("  Sin ventas registradas")
            return

        total = len(self.sales)

        # reduce + lambda: ingreso total acumulado.
        total_revenue = reduce(lambda acc, s: acc + s["total"], self.sales, 0)

        avg_sale = total_revenue / total

        # reduce + lambda: venta de mayor monto.
        max_sale = reduce(
            lambda a, b: a if a["total"] >= b["total"] else b,
            self.sales
        )

        # comprehension: IDs de ventas por encima del promedio.
        above_avg_ids = [s["sale_id"] for s in self.sales if s["total"] > avg_sale]

        # reduce con comprehension anidada: total de unidades vendidas.
        total_units = reduce(
            lambda acc, s: acc + sum(item["quantity"] for item in s["items"]),
            self.sales,
            0
        )

        # dict comprehension: unidades vendidas por producto (agregado).
        all_items = [item for s in self.sales for item in s["items"]]
        product_names = {item["name"] for item in all_items}
        units_by_product = {
            name: reduce(
                lambda acc, it: acc + (it["quantity"] if it["name"] == name else 0),
                all_items,
                0
            )
            for name in product_names
        }

        # max sobre items() con lambda como key: producto más vendido.
        top_product = max(units_by_product.items(), key=lambda kv: kv[1])

        print(f"  Total ventas registradas: {total}")
        print(f"  Ingreso total: {total_revenue:.2f}")
        print(f"  Venta promedio: {avg_sale:.2f}")
        print(f"  Venta más alta: #{max_sale['sale_id']} ({max_sale['total']:.2f})")
        print(f"  Ventas por encima del promedio: {above_avg_ids if above_avg_ids else '—'}")
        print(f"  Unidades totales vendidas: {total_units}")
        print(f"  Unidades por producto: {units_by_product}")
        print(f"  Producto más vendido: {top_product[0]} ({top_product[1]} unid.)")
