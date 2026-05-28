# ============================================================
# app.py
# ------------------------------------------------------------
# Punto de entrada de la aplicación.
# Ejecutar este archivo inicia la interfaz gráfica.
#
# Estructura del proyecto:
#   app.py                        → punto de entrada
#   estadistica_app/
#       __init__.py               → marca la carpeta como módulo
#       config.py                 → colores, constantes, mapeos
#       state.py                  → estado centralizado (AppState)
#       data_service.py           → carga y limpieza del Excel
#       stats_service.py          → cálculos estadísticos
#       plot_service.py           → generación de gráficas
#       ui_helpers.py             → widgets reutilizables (make_card, btn)
#       main_window.py            → ventana principal y lógica de UI
#
# Para ejecutar:
#   python app.py
#
# Requisitos (instalar con: pip install -r requirements.txt):
#   pandas, numpy, matplotlib, scipy, openpyxl
# ============================================================
 
from estadistica_app.main_window import iniciar_app
 
 
if __name__ == "__main__":
    iniciar_app()