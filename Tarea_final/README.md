# Sistema de Gestión de Permisos de Personal

Aplicación de consola en Python que permite gestionar **empleados**, **tipos de permiso** y **permisos**, persistiendo la información en archivos JSON. Construida como práctica de Programación Orientada a Objetos aplicando herencia múltiple, mixins, interfaces abstractas, decoradores, programación funcional y separación por capas MVC.

---

## 1. Estructura del proyecto (MVC)

```
Practica2/
├── main.py                          # Punto de entrada
├── README.md
│
├── models/                          # M — Entidades de dominio
│   ├── __init__.py
│   ├── employee.py                  # Modelo Empleado
│   ├── leave_type.py                # Modelo Tipo de Permiso
│   └── leave.py                     # Modelo Permiso
│
├── views/                           # V — Capa de presentación (menús)
│   ├── __init__.py
│   └── menu.py                      # Menú principal y submenús
│
├── controllers/                     # C — Lógica de negocio
│   ├── __init__.py
│   ├── employee_controller.py       # CRUD de empleados
│   ├── leave_type_controller.py     # CRUD de tipos de permiso
│   ├── leave_controller.py          # CRUD de permisos
│   └── stats_controller.py          # Estadísticas del sistema
│
├── core/                            # Infraestructura transversal
│   ├── __init__.py
│   ├── interfaces.py                # CrudInterface (ABC)
│   ├── mixins.py                    # ValidationMixin, LogMixin
│   ├── decorators.py                # ask_continue, confirm_save
│   ├── json_manager.py              # Persistencia JSON
│   └── console.py                   # Colores ANSI, tablas, gotoxy, clear
│
└── data/                            # Datos persistidos
    ├── employees.json
    ├── leave_types.json
    └── leaves.json
```

---

## 2. Arquitectura por capas (MVC)

```
┌─────────────────────────────────────────────────────┐
│  main.py  →  views/Menu         (V — Presentación)  │
└────────────────────────┬────────────────────────────┘
                         │ delega operaciones
                         ▼
┌─────────────────────────────────────────────────────┐
│  controllers/                   (C — Negocio)       │
│  - EmployeeController                               │
│  - LeaveTypeController                              │
│  - LeaveController                                  │
│  - StatsController                                  │
└────────────────────────┬────────────────────────────┘
                         │ opera sobre
                         ▼
┌─────────────────────────────────────────────────────┐
│  models/                        (M — Dominio)       │
│  - Employee / LeaveType / Leave                     │
└────────────────────────┬────────────────────────────┘
                         │ persiste mediante
                         ▼
┌─────────────────────────────────────────────────────┐
│  core/JsonManager               (Persistencia)      │
└────────────────────────┬────────────────────────────┘
                         │ lee/escribe
                         ▼
              data/employees.json
              data/leave_types.json
              data/leaves.json
```

**Paquete `core/` (infraestructura transversal):**
- `interfaces.py` — `CrudInterface` (ABC) con `create / read / update / delete`.
- `mixins.py` — `ValidationMixin` (7 validaciones) y `LogMixin` (mensajes de log).
- `decorators.py` — `ask_continue` (repetición en bucle) y `confirm_save` (confirmación 1/2).
- `json_manager.py` — `initialize`, `load` y `save` de archivos JSON.
- `console.py` — colores ANSI, `gotoxy`, `clear`, `print_table` y helpers de presentación.

---

## 3. Modelos de dominio

### `Employee`
| Atributo | Tipo | Descripción |
|---|---|---|
| `employee_id` | int | Identificador (privado, solo lectura) |
| `name` | str | Nombre del empleado |
| `cedula` | str | Cédula ecuatoriana (validada módulo 10) |
| `salary` | float | Sueldo mensual |

- **Property calculada:** `hourly_rate` = `salary / 240` (horas laborables al mes)
- **Constante estática:** `WORK_HOURS_MONTH = 240`

### `LeaveType`
| Atributo | Tipo | Descripción |
|---|---|---|
| `leave_type_id` | int | Identificador (privado, solo lectura) |
| `description` | str | Descripción del tipo de permiso |
| `is_paid` | str | `"S"` = remunerado / `"N"` = no remunerado |

- **Constantes:** `PAID = "S"` / `UNPAID = "N"`
- **Property:** `affects_salary` → `True` si `is_paid == "N"`

### `Leave`
| Atributo | Tipo | Descripción |
|---|---|---|
| `leave_id` | int | Identificador (privado, solo lectura) |
| `employee` | dict | Datos del empleado embebidos |
| `leave_type` | dict | Datos del tipo de permiso embebidos |
| `date_from` | str | Fecha inicio `"YYYY-MM-DD"` |
| `date_until` | str | Fecha fin `"YYYY-MM-DD"` |
| `duration_type` | str | `"D"` = días / `"H"` = horas |
| `tiempo` | float | Cantidad de días u horas del permiso |

- **Constantes:** `TYPE_DAYS = "D"` / `TYPE_HOURS = "H"`
- **Property:** `affects_salary` → consulta `is_paid` del tipo embebido

---

## 4. Infraestructura (core/)

### Validaciones disponibles (`ValidationMixin`)

| Método | Descripción | Usado en |
|---|---|---|
| `validate_not_empty` | Campo no vacío | Los 3 controladores |
| `validate_positive_number` | Número > 0 | EmployeeController, LeaveController |
| `validate_date` | Formato `YYYY-MM-DD` | LeaveController |
| `validate_duration_type` | Solo `"D"` o `"H"` | LeaveController |
| `validate_cedula_ecuatoriana` | Módulo 10, provincia 01–24 | EmployeeController |
| `validate_only_letters` | Solo letras y espacios | EmployeeController |
| `validate_numeric` | Valor convertible a float | EmployeeController |

### Decoradores (`decorators.py`)

- **`@ask_continue(message)`** — repite la función en bucle mientras el usuario responda `"s"`, acumulando resultados distintos de `None`.
- **`@confirm_save(message)`** — solicita confirmación numérica `1=Sí / 2=No` antes de ejecutar la función. Si el usuario elige `2`, la función no se ejecuta.

### Persistencia (`JsonManager`)

| Método | Descripción |
|---|---|
| `initialize()` | Crea el archivo JSON con `[]` si no existe. Si existe, pasa de largo. |
| `load()` | Lee el JSON y retorna lista. Si no existe el archivo, retorna `[]`. |
| `save(data)` | Escribe el JSON con `indent=4` y `ensure_ascii=False`. Crea `data/` si no existe. |

---

## 5. Flujo general de ejecución

### 5.1 Arranque

`main.py` inicializa los archivos JSON y lanza el menú principal:

```python
from core import JsonManager
from views import Menu

JsonManager("data/employees.json").initialize()
JsonManager("data/leave_types.json").initialize()
JsonManager("data/leaves.json").initialize()

app = Menu()
app.main_menu()
```

### 5.2 Menú principal

```
█|█|█|█|█|█|█|█|█|█|█|█|█|█|█|█|█|█|█|█|█|█|
█|         SISTEMA DE PERMISOS              █|
█|█|█|█|█|█|█|█|█|█|█|█|█|█|█|█|█|█|█|█|█|█|

  1. Empleados
  2. Tipos de Permiso
  3. Permisos
  4. Estadísticas
  0. Salir
```

### 5.3 Submenús CRUD

| Opción | Acción | Comportamiento |
|:---:|---|---|
| 1 | Registrar | Validación campo por campo con reintento en bucle |
| 2 | Listar | Tabla alineada con colores por celda |
| 3 | Eliminar | Muestra tabla resumida → pide ID → elimina |
| 0 | Volver | — |

### 5.4 Flujo de registro de permiso

```
Usuario → leave_menu → create()
                           │
          ┌────────────────┼─────────────────┐
          ▼                ▼                 ▼
  _select_employee   _select_leave_type   inputs fechas/tiempo
  (recarga JSON)     (recarga JSON)       + validaciones
          │                │                 │
          └────────────────┴────────────────-┘
                           │
                    _calc_deduction()
                    _print_summary()
                    Confirmar 1/2
                           │
                    Leave.to_dict()
                    JsonManager.save()
                    leaves.json
```

---

## 6. Modelo de datos (JSON)

### `employees.json`
```json
[
  {
    "employee_id": 1,
    "name": "Juan Pérez",
    "cedula": "0954761078",
    "salary": 1500.0
  }
]
```

### `leave_types.json`
```json
[
  {
    "leave_type_id": 1,
    "description": "Vacaciones",
    "is_paid": "S"
  },
  {
    "leave_type_id": 2,
    "description": "Permiso personal",
    "is_paid": "N"
  }
]
```

### `leaves.json`
```json
[
  {
    "leave_id": 1,
    "employee": {
      "employee_id": 1,
      "name": "Juan Pérez",
      "cedula": "0954761078",
      "salary": 1500.0
    },
    "leave_type": {
      "leave_type_id": 2,
      "description": "Permiso personal",
      "is_paid": "N"
    },
    "date_from": "2026-05-01",
    "date_until": "2026-05-03",
    "duration_type": "D",
    "tiempo": 3.0
  }
]
```

---

## 7. Conceptos POO aplicados

| Concepto | Dónde |
|---|---|
| **Encapsulamiento** | Atributos privados `_id` con properties de solo lectura en los 3 modelos |
| **Herencia múltiple** | `EmployeeController(CrudInterface, ValidationMixin, LogMixin)` |
| **Interfaces abstractas** | `CrudInterface` con `@abstractmethod` para los 4 métodos CRUD |
| **Mixins** | `ValidationMixin` y `LogMixin` reutilizados en los 3 controladores |
| **Decoradores** | `ask_continue` y `confirm_save` en `core/decorators.py` con `@wraps` |
| **Programación funcional** | `map`, `filter`, `reduce` y `lambda` en `StatsController` |
| **Separación de capas** | `views/` ↔ `controllers/` ↔ `models/` ↔ `core/` |
| **Serialización** | `to_dict()` y `from_dict()` en cada modelo para persistencia JSON |

---

## 8. Estadísticas del sistema

`StatsController` genera un reporte con:

**Empleados:**
- Total, nombres, masa salarial, sueldo promedio, mejor remunerado
- Valor/hora por empleado (impreso verticalmente)

**Tipos de permiso:**
- Total, remunerados vs no remunerados con sus nombres

**Permisos:**
- Total, remunerados vs no remunerados
- Total tiempo solicitado, total descuentos generados
- Tiempo por empleado (impreso verticalmente)
- Empleado con más tiempo de permiso

---

## 9. Ejecución

Desde la raíz del proyecto:

```bash
python main.py
```

No requiere dependencias externas: utiliza únicamente módulos de la librería estándar (`json`, `os`, `abc`, `functools`, `datetime`).

---

## 10. Interfaz visual

La consola usa códigos ANSI implementados en `core/console.py` sin librerías externas:

- **Colores por intención:** verde=registrar, amarillo=tipos de permiso, magenta=permisos, cyan=consultar, rojo=eliminar
- **Separador:** patrón `█|` con fondo morado en títulos
- **Tablas:** columnas alineadas automáticamente con colores por celda
- **`gotoxy(x, y)`:** posicionamiento de cursor al estilo Turbo C
- **`clear()`:** borrado de pantalla compatible Windows/Linux/Mac
