from datetime import datetime
from models import Leave


class ValidationMixin:
    @staticmethod
    def validate_not_empty(value, field_name):
        if not value.strip():
            raise ValueError(f"{field_name} no puede estar vacío")

    @staticmethod
    def validate_positive_number(value, field_name):
        if value <= 0:
            raise ValueError(f"{field_name} debe ser mayor a 0")

    @staticmethod
    def validate_date(value, field_name):
        try:
            datetime.strptime(value.strip(), "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"{field_name} debe tener el formato YYYY-MM-DD y ser una fecha válida")

    @staticmethod
    def validate_duration_type(value):
        if value not in (Leave.TYPE_DAYS, Leave.TYPE_HOURS):
            raise ValueError("Modalidad inválida. Use 'D' para días o 'H' para horas")

    @staticmethod
    def validate_cedula_ecuatoriana(cedula):
        cedula = cedula.strip()

        if not cedula.isdigit() or len(cedula) != 10:
            raise ValueError("La cédula debe contener exactamente 10 dígitos numéricos")

        provincia = int(cedula[:2])
        if provincia < 1 or provincia > 24:
            raise ValueError("La cédula tiene un código de provincia inválido (debe ser 01–24)")

        coeficientes   = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        digito_real    = int(cedula[9])
        suma           = 0

        for i, coef in enumerate(coeficientes):
            valor = int(cedula[i]) * coef
            if valor >= 10:
                valor -= 9
            suma += valor

        digito_calculado = (10 - (suma % 10)) % 10

        if digito_real != digito_calculado:
            raise ValueError("La cédula ingresada no es válida (dígito verificador incorrecto)")


    @staticmethod
    def validate_only_letters(value, field_name):
        if not all(c.isalpha() or c.isspace() for c in value.strip()):
            raise ValueError(f"{field_name} solo puede contener letras y espacios")

    @staticmethod
    def validate_numeric(value, field_name):
        try:
            float(value)
        except ValueError:
            raise ValueError(f"{field_name} debe ser un valor numérico")


class LogMixin:
    LOG_PREFIX = "[LOG]"

    def log(self, message):
        print(f"{LogMixin.LOG_PREFIX}: {message}")
