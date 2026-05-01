# Mixin de validaciones reutilizables para los modelos y controladores.
# Las validaciones son métodos estáticos: no dependen del estado de la instancia,
# pero se exponen como mixin para inyectarlas vía herencia múltiple.
class ValidationMixin:
    # Verifica que una cadena no esté vacía ni contenga solo espacios.
    @staticmethod
    def validate_not_empty(value, field_name):
        if not value.strip():
            raise ValueError(f"{field_name} no puede estar vacío")

    # Verifica que un valor numérico sea estrictamente mayor que cero.
    @staticmethod
    def validate_positive_number(value, field_name):
        if value <= 0:
            raise ValueError(f"{field_name} debe ser mayor a 0")


# Mixin de registro: imprime mensajes informativos por consola.
class LogMixin:
    # Prefijo estático compartido por todas las instancias.
    LOG_PREFIX = "[LOG]"

    def log(self, message):
        print(f"{LogMixin.LOG_PREFIX}: {message}")
