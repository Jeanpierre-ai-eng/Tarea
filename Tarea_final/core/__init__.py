# Paquete de infraestructura transversal: persistencia, interfaces, mixins, decoradores y consola.
from .decorators import ask_continue, confirm_save
from .interfaces import CrudInterface
from .json_manager import JsonManager
from .mixins import ValidationMixin, LogMixin
from .console import (
    Color,
    gotoxy,
    clear,
    print_header,
    print_separator,
    print_success,
    print_error,
    print_warning,
    print_info,
    print_option,
    input_prompt,
    print_table,
)

__all__ = [
    "ask_continue",
    "confirm_save",
    "CrudInterface",
    "JsonManager",
    "ValidationMixin",
    "LogMixin",
    "Color",
    "gotoxy",
    "clear",
    "print_header",
    "print_separator",
    "print_success",
    "print_error",
    "print_warning",
    "print_info",
    "print_option",
    "input_prompt",
    "print_table",
]