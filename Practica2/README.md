# Sistema de Ventas con JSON

Aplicación de consola en Python que permite gestionar **clientes**, **productos** y **ventas**, persistiendo la información en archivos JSON. Construida como práctica de Programación Orientada a Objetos aplicando herencia, mixins, interfaces abstractas y separación por capas.

---

## 1. Estructura del proyecto (MVC)

```
Practica2/
├── main.py                       # Punto de entrada
├── README.md
│
├── models/                       # M — Entidades de dominio
│   ├── __init__.py
│   ├── customer.py
│   ├── product.py
│   └── sale.py
│
├── views/                        # V — Capa de presentación (menús)
│   ├── __init__.py
│   └── menu.py
│
├── controllers/                  # C — Lógica de negocio
│   ├── __init__.py
│   ├── customer_controller.py
│   ├── product_controller.py
│   └── sale_controller.py
│
├── core/                         # Infraestructura transversal
│   ├── __init__.py
│   ├── interfaces.py             # CrudInterface (ABC)
│   ├── mixins.py                 # ValidationMixin, LogMixin
│   └── json_manager.py           # Persistencia JSON
│
└── data/                         # Datos persistidos
    ├── customers.json
    ├── products.json
    └── sales.json
```

---

## 2. Arquitectura por capas (MVC)

El proyecto aplica el patrón **Modelo–Vista–Controlador**:

```
┌────────────────────────────────────────────────────┐
│  main.py  →  views/Menu        (V — Presentación)  │
└────────────────────────┬───────────────────────────┘
                         │ delega operaciones
                         ▼
┌────────────────────────────────────────────────────┐
│  controllers/                  (C — Negocio)       │
│  - CustomerController                              │
│  - ProductController                               │
│  - SaleController                                  │
└────────────────────────┬───────────────────────────┘
                         │ opera sobre
                         ▼
┌────────────────────────────────────────────────────┐
│  models/                       (M — Dominio)       │
│  - Customer / Product / Sale                       │
└────────────────────────┬───────────────────────────┘
                         │ persiste mediante
                         ▼
┌────────────────────────────────────────────────────┐
│  core/JsonManager              (Persistencia)      │
└────────────────────────┬───────────────────────────┘
                         │ lee/escribe
                         ▼
              data/customers.json
              data/products.json
              data/sales.json
```

**Paquete `core/` (infraestructura transversal):**
- `interfaces.py` — `CrudInterface` (ABC) con `create / read / update / delete`.
- `mixins.py` — `ValidationMixin` (validaciones) y `LogMixin` (mensajes de log).
- `json_manager.py` — lectura y escritura de archivos JSON.

---

## 3. Flujo general de ejecución

### 3.1 Arranque

[main.py](main.py) instancia la clase `Menu` (paquete `views`) y llama a `main_menu()`:

```python
from views import Menu

app = Menu()
app.main_menu()
```

### 3.2 Menú principal

`Menu.main_menu()` muestra las opciones y dirige a los submenús correspondientes:

```
==============================
 SISTEMA DE VENTAS CON JSON
==============================
1. Clientes
2. Productos
3. Ventas
0. Salir
```

Cada opción invoca un submenú dedicado.

### 3.3 Submenús CRUD (Clientes y Productos)

Tanto `customer_menu()` como `product_menu()` siguen el mismo patrón CRUD:

| Opción | Acción            | Controlador invocado         |
|:------:|-------------------|------------------------------|
|   1    | Crear             | `controller.create()`        |
|   2    | Listar            | `controller.read()`          |
|   3    | Actualizar        | `controller.update()`        |
|   4    | Eliminar          | `controller.delete()`        |
|   0    | Volver al menú    | —                            |

Los controladores (`CustomerController`, `ProductController`) heredan de `CrudInterface`, `ValidationMixin` y `LogMixin`, garantizando uniformidad y validaciones consistentes (campos no vacíos, números positivos).

### 3.4 Submenú de Ventas

`sale_menu()` orquesta el registro de ventas separando claramente la presentación del servicio:

1. **Selección de cliente** (`_select_customer`)
   - Muestra el listado de clientes disponibles: `ID - Nombre`.
   - Solicita el ID del cliente.
   - Verifica existencia con `SaleController.find_customer()`.

2. **Selección de productos** (`_select_items`)
   - Muestra los productos disponibles con su stock: `ID - Nombre (stock: N)`.
   - Solicita el ID del producto y la cantidad.
   - Valida que la cantidad no exceda el stock.
   - Permite agregar varios productos en bucle.

3. **Persistencia** (`SaleController.register_sale`)
   - Calcula subtotal de los ítems.
   - Aplica IVA del 15 % (`IVA_RATE = 0.15`).
   - Calcula total final.
   - Crea instancia de `Sale` y la guarda en `sales.json`.
   - Actualiza el stock de productos en `products.json`.
   - Imprime el resumen: subtotal, IVA y total.

---

## 4. Modelo de datos (JSON)

### `customers.json`
```json
[
  { "customer_id": 1, "name": "Juan Pérez", "identification": "0102030405" }
]
```

### `products.json`
```json
[
  { "product_id": 1, "name": "Camiseta", "price": 15.0, "stock": 50 }
]
```

### `sales.json`
```json
[
  {
    "sale_id": 1,
    "customer": { "customer_id": 1, "name": "Juan Pérez", "identification": "0102030405" },
    "items": [
      { "product_id": 1, "name": "Camiseta", "price": 15.0, "quantity": 2, "subtotal": 30.0 }
    ],
    "subtotal": 30.0,
    "iva": 4.5,
    "total": 34.5
  }
]
```

---

## 5. Conceptos POO aplicados

| Concepto                | Dónde                                                                 |
|-------------------------|------------------------------------------------------------------------|
| **Encapsulamiento**     | Cada modelo expone solo lo necesario y delega persistencia al servicio.|
| **Herencia múltiple**   | `CustomerController(CrudInterface, ValidationMixin, LogMixin)`         |
| **Interfaces abstractas** | `CrudInterface` con `@abstractmethod` para `create/read/update/delete`. |
| **Mixins**              | `ValidationMixin`, `LogMixin` reutilizados en varios servicios.        |
| **Separación de capas** | Presentación (`views/`) ↔ Negocio (`controllers/`) ↔ Persistencia (`core/json_manager.py`). |
| **Serialización**       | Cada modelo implementa `to_dict()` para conversión a JSON.             |

---

## 6. Ejecución

Desde la raíz del proyecto:

```bash
python main.py
```

No requiere dependencias externas: utiliza únicamente módulos de la librería estándar (`json`, `os`, `abc`).

---

## 7. Flujo resumido de una venta

```
Usuario → main_menu → sale_menu → _create_sale_flow
                                       │
                  ┌────────────────────┼────────────────────┐
                  ▼                    ▼                    ▼
          _select_customer       _select_items       register_sale
          (lista clientes)       (lista productos)   (calcula IVA,
                                  + stock)            persiste venta y
                                                      actualiza stock)
                                                            │
                                                            ▼
                                                   sales.json + products.json
```
