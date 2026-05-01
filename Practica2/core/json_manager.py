import json
import os


class JsonManager:
    """Gestor de persistencia para almacenar y recuperar datos en formato JSON."""

    def __init__(self, filename):
        # Ruta del archivo JSON sobre el cual se realizarán las operaciones.
        self.filename = filename

    def load(self):
        """Carga y retorna el contenido del archivo JSON.

        Si el archivo no existe, retorna una lista vacía para evitar errores
        en la primera ejecución del programa.
        """
        if not os.path.exists(self.filename):
            return []

        with open(self.filename, "r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, data):
        """Guarda los datos proporcionados en el archivo JSON.

        Se utiliza indentación de 4 espacios para mejorar la legibilidad y
        ensure_ascii=False para conservar caracteres especiales (tildes, ñ, etc.).
        """
        # Crea el directorio destino si no existe (útil para data/).
        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
