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
