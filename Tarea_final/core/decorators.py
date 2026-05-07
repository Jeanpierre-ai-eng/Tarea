from functools import wraps


def ask_continue(message="¿Desea continuar? (s/n): "):
    def decorator(func):
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
