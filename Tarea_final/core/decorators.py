# Decoradores transversales reutilizables por la capa de vistas y controladores.
from functools import wraps


# Repite la ejecución de la función decorada mientras el usuario responda 's'
# al mensaje de confirmación. Los retornos distintos de None se acumulan en
# una lista que se devuelve al finalizar el bucle.
def ask_continue(message="¿Desea continuar? (s/n): "):
    def decorator(func):
        # wraps preserva el nombre y docstring de la función original.
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            while True:
                result = func(*args, **kwargs)
                if result is not None:
                    results.append(result)
                if input(message).strip().lower() != "s":
                    break
            return results
        return wrapper
    return decorator

# Solicita confirmación numérica (1=Sí / 2=No) antes de ejecutar la función decorada.
# Si el usuario elige 2 o cualquier opción inválida, la operación se cancela
# y la función no se ejecuta. Usado en los flujos de registro de la capa de vistas.
def confirm_save(message="¿Desea guardar?\n1. Sí\n2. No\nOpción: "):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            opcion = input(message).strip()
            if opcion == "1":
                return func(*args, **kwargs)
            else:
                print("Operación cancelada.")
        return wrapper
    return decorator
