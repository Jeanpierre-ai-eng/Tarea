from abc import ABC, abstractmethod

"""
Módulo de interfaces CRUD.
Define el contrato para operaciones básicas de gestión de datos.
"""


class CrudInterface(ABC):
    """
    Interfaz abstracta que define las operaciones CRUD.
    Toda clase que ofrezca creación, lectura, actualización y eliminación
    de registros debe implementar este contrato.
    """

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass
