# Punto de entrada de la aplicación.
# Instancia el menú principal (capa de vistas) y delega en él el flujo de ejecución.
from views import Menu

app = Menu()
app.main_menu()
