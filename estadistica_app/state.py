# ============================================================
# state.py
# ------------------------------------------------------------
# Define la clase AppState, que centraliza todo el estado
# mutable de la aplicación.
#
# En lugar de usar variables globales dispersas por el código,
# se usa un único objeto `state` que se pasa a las funciones
# que lo necesitan. Esto hace el código más ordenado y
# evita errores difíciles de rastrear.
# ============================================================


class AppState:
    """
    Contiene el estado completo de la aplicación en un momento dado.

    Atributos principales:
        data           → DataFrame con los datos del Excel cargado
        mu, sigma      → media y desviación estándar de la variable numérica activa
        columna_activa → nombre de la columna numérica seleccionada para análisis
        mu_bin         → media calculada con la aproximación binomial (μ = n·p)
        sigma_bin      → desviación estándar binomial (σ = √(n·p·q))
        modo_activo    → "normal" o "binomial", controla qué secciones están activas
    """

    def __init__(self):
        # Datos del Excel (pandas DataFrame)
        self.data = None

        # Parámetros del módulo normal (variable numérica)
        self.mu             = None   # Media aritmética
        self.sigma          = None   # Desviación estándar
        self.columna_activa = None   # Columna seleccionada (ej. "Edad")

        # Parámetros del módulo binomial → normal
        self.mu_bin    = None   # μ = n * p
        self.sigma_bin = None   # σ = √(n * p * q)

        # Modo de operación activo
        self.modo_activo = None


    def reiniciar_normal(self):
        """
        Limpia los parámetros del módulo de variable numérica.
        Se llama cuando se carga un nuevo archivo o se cambia de modo.
        """
        self.mu             = None
        self.sigma          = None
        self.columna_activa = None


    def reiniciar_binomial(self):
        """
        Limpia los parámetros del módulo binomial → normal.
        Se llama cuando se carga un nuevo archivo o se cambia de modo.
        """
        self.mu_bin    = None
        self.sigma_bin = None


    def reiniciar_todo(self):
        """
        Resetea completamente la aplicación a su estado inicial.
        Equivale a un "nuevo proyecto" sin cerrar la ventana.
        """
        self.data = None
        self.reiniciar_normal()
        self.reiniciar_binomial()
        self.modo_activo = None