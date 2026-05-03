# Mixin de validaciones reutilizables para los modelos y controladores.
# Las validaciones son métodos estáticos: no dependen del estado de la instancia,
# pero se exponen como mixin para inyectarlas vía herencia múltiple.
from datetime import datetime
from models import Leave


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

    # Verifica que la cadena corresponda a una fecha real en formato YYYY-MM-DD.
    # Consistente con el formato usado en leave_controller.py y stats_controller.py.
    @staticmethod
    def validate_date(value, field_name):
        try:
            datetime.strptime(value.strip(), "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"{field_name} debe tener el formato YYYY-MM-DD y ser una fecha válida")

    # Verifica que la modalidad del permiso sea 'D' (días) o 'H' (horas).
    # Centraliza la lógica que antes estaba hardcodeada en leave_controller.py.
    @staticmethod
    def validate_duration_type(value):
        if value not in (Leave.TYPE_DAYS, Leave.TYPE_HOURS):
            raise ValueError("Modalidad inválida. Use 'D' para días o 'H' para horas")

    # Valida una cédula ecuatoriana usando el algoritmo módulo 10.
    # Reglas:
    #   1. Debe tener exactamente 10 dígitos numéricos.
    #   2. Los dos primeros dígitos (provincia) deben estar entre 01 y 24.
    #   3. El dígito verificador (posición 9) se calcula sobre los primeros 9 dígitos.
    @staticmethod
    def validate_cedula_ecuatoriana(cedula):
        cedula = cedula.strip()

        # Regla 1: exactamente 10 dígitos numéricos.
        if not cedula.isdigit() or len(cedula) != 10:
            raise ValueError("La cédula debe contener exactamente 10 dígitos numéricos")

        # Regla 2: código de provincia válido (01 – 24).
        provincia = int(cedula[:2])
        if provincia < 1 or provincia > 24:
            raise ValueError("La cédula tiene un código de provincia inválido (debe ser 01–24)")

        # Regla 3: dígito verificador por módulo 10.
        coeficientes   = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        digito_real    = int(cedula[9])
        suma           = 0

        for i, coef in enumerate(coeficientes):
            valor = int(cedula[i]) * coef
            # Si el producto es >= 10, se restan 9 (equivalente a sumar sus dígitos).
            if valor >= 10:
                valor -= 9
            suma += valor

        digito_calculado = (10 - (suma % 10)) % 10

        if digito_real != digito_calculado:
            raise ValueError("La cédula ingresada no es válida (dígito verificador incorrecto)")


    # Verifica que una cadena contenga solo letras y espacios (sin números ni símbolos).
    @staticmethod
    def validate_only_letters(value, field_name):
        if not all(c.isalpha() or c.isspace() for c in value.strip()):
            raise ValueError(f"{field_name} solo puede contener letras y espacios")

    # Verifica que una cadena pueda convertirse a número flotante positivo.
    @staticmethod
    def validate_numeric(value, field_name):
        try:
            float(value)
        except ValueError:
            raise ValueError(f"{field_name} debe ser un valor numérico")


# Mixin de registro: imprime mensajes informativos por consola.
class LogMixin:
    # Prefijo estático compartido por todas las instancias.
    LOG_PREFIX = "[LOG]"

    def log(self, message):
        print(f"{LogMixin.LOG_PREFIX}: {message}")
