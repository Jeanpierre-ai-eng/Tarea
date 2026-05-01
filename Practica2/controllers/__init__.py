# Paquete de controladores: encapsulan la lógica de negocio del sistema.
from .customer_controller import CustomerController
from .product_controller import ProductController
from .sale_controller import SaleController
from .stats_controller import StatsController

__all__ = [
    "CustomerController",
    "ProductController",
    "SaleController",
    "StatsController",
]
