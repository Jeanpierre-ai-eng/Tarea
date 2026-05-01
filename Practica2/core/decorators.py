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
