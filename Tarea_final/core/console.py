# Utilidades de consola: colores ANSI, fondos, posicionamiento y tablas.
# No requiere librerías externas — usa únicamente códigos de escape ANSI y os.
import os

ESC = '\x1b'

# ── Texto ─────────────────────────────────────────────────────────────────────
class Color:
    RESET   = ESC + '[0m'
    BOLD    = ESC + '[1m'

    # Texto
    WHITE   = ESC + '[37m'
    CYAN    = ESC + '[36m'
    GREEN   = ESC + '[32m'
    RED     = ESC + '[31m'
    YELLOW  = ESC + '[33m'
    GRAY    = ESC + '[90m'

    # Texto brillante
    BCYAN   = ESC + '[96m'
    BGREEN  = ESC + '[92m'
    BRED    = ESC + '[91m'
    BYELLOW = ESC + '[93m'
    BWHITE   = ESC + '[97m'
    BMAGENTA = ESC + '[95m'
    BBLUE    = ESC + '[94m'
    ORANGE   = ESC + '[38;5;208m'
    PINK     = ESC + '[38;5;213m'

    # Fondos
    BG_BLUE   = ESC + '[44m'
    BG_GREEN  = ESC + '[42m'
    BG_RED    = ESC + '[41m'
    BG_YELLOW = ESC + '[43m'
    BG_PURPLE = ESC + '[45m'
    BG_CYAN   = ESC + '[46m'

    @staticmethod
    def paint(text, *codes):
        """Aplica uno o más códigos ANSI al texto y resetea al final."""
        return "".join(codes) + text + Color.RESET


# ── Separadores ───────────────────────────────────────────────────────────────
SEP_WIDTH  = 55
SEP_PATRON = "█|"

def _separator():
    """Genera una línea separadora con el patrón ___|||."""
    repeat = (SEP_WIDTH // len(SEP_PATRON)) + 1
    return (SEP_PATRON * repeat)[:SEP_WIDTH]


# ── Utilidades de pantalla ────────────────────────────────────────────────────
def gotoxy(x, y):
    """Mueve el cursor a la posición (columna x, fila y) en la terminal."""
    print(f"\033[{y};{x}H", end="", flush=True)


def clear():
    """Borra el contenido visible de la terminal."""
    os.system("cls" if os.name == "nt" else "clear")


# ── Bloques de presentación ───────────────────────────────────────────────────
def print_header(title, bg=Color.BG_PURPLE):
    """Encabezado con marco █| a los lados y fondo morado en el título."""
    sep    = Color.paint(_separator(), Color.BCYAN)
    marco  = Color.paint("█|", Color.BCYAN)
    centro = Color.paint(title.center(SEP_WIDTH - 4), Color.BOLD, Color.WHITE, Color.BG_PURPLE)
    print(sep)
    print(f"{marco}{centro}{marco}")
    print(sep)


def print_separator():
    """Línea separadora simple."""
    print(Color.paint(_separator(), Color.BCYAN))


def print_success(message):
    print(Color.paint(f"  ✔  {message}", Color.BGREEN))


def print_error(message):
    print(Color.paint(f"  ✘  {message}", Color.BRED))


def print_warning(message):
    print(Color.paint(f"  ⚠  {message}", Color.BYELLOW))


def print_info(message):
    print(Color.paint(f"  ℹ  {message}", Color.BCYAN))


def print_option(key, label, bg=Color.BG_GREEN, fg=Color.BGREEN):
    """Imprime una opción de menú con número y texto en negrita, sin fondos."""
    num   = Color.paint(f" {key}.", Color.BOLD, fg)
    texto = Color.paint(f" {label}", Color.BOLD, fg)
    print(f"  {num}{texto}")


def input_prompt(label="Opción"):
    """Input con estilo."""
    return input(Color.paint(f"  {label}: ", Color.BOLD, Color.BWHITE))


# ── Tablas ────────────────────────────────────────────────────────────────────
def _table_row(cols, widths, color=Color.WHITE):
    """Genera una fila de tabla con columnas alineadas."""
    cells = " │ ".join(str(c).ljust(w) for c, w in zip(cols, widths))
    print(Color.paint(f" {cells} ", color))


def _table_divider(widths, char="─", mid="┼"):
    """Genera una línea divisora de tabla."""
    parts = (char * (w + 2) for w in widths)
    print(Color.paint(f"{'─' + mid}".join(parts) + "─", Color.CYAN))


def print_table(headers, rows, col_colors=None):
    """
    Imprime una tabla alineada en consola.

    headers   : lista de encabezados
    rows      : lista de listas con los datos
    col_colors: dict {col_index: color} para colorear columnas específicas
    """
    # Calcula el ancho de cada columna.
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    # Encabezado de tabla.
    _table_row(headers, widths, Color.CYAN)
    _table_divider(widths)

    # Filas de datos.
    for row in rows:
        if col_colors:
            # Imprime celda por celda aplicando color individual si corresponde.
            cells = []
            for i, (cell, w) in enumerate(zip(row, widths)):
                color = col_colors.get(i, Color.WHITE)
                cells.append(Color.paint(str(cell).ljust(w), color))
            print(Color.paint(" ", Color.RESET) + " │ ".join(cells))
        else:
            _table_row(row, widths)

    _table_divider(widths, char="─", mid="┴")
    print(Color.paint(f"  {len(rows)} registro(s)", Color.GRAY))