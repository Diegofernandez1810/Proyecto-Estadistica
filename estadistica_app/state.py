class AppState:
    def __init__(self):
        self.data = None

        self.mu = None
        self.sigma = None
        self.columna_activa = None

        self.mu_bin = None
        self.sigma_bin = None

        self.modo_activo = None

    def reiniciar_normal(self):
        self.mu = None
        self.sigma = None
        self.columna_activa = None

    def reiniciar_binomial(self):
        self.mu_bin = None
        self.sigma_bin = None

    def reiniciar_todo(self):
        self.data = None
        self.reiniciar_normal()
        self.reiniciar_binomial()
        self.modo_activo = None