class Oferta:
    def __init__(self, semestre: str, vagas: int, local: str = ""):
        if vagas < 0:
            raise ValueError("Número de vagas deve ser >= 0.")
        self._semestre = semestre
        self.vagas = vagas
        self._local = local
        self._aberta = True

    @property
    def semestre(self):
        return self._semestre
    @semestre.setter
    def semestre(self, valor):

        if not valor.strip():
         raise ValueError(
            "Semestre não pode ser vazio."
        )
        self._semestre = valor

    @property
    def vagas(self):
        return self._vagas

    @vagas.setter
    def vagas(self, valor: int):
        if valor < 0:
            raise ValueError("Número de vagas deve ser >= 0.")
        self._vagas = valor

    @property
    def local(self):
        return self._local
    @local.setter
    def local(self, valor):
      self._local = valor

    @property
    def aberta(self):
        return self._aberta

    def abrir(self):
        self._aberta = True

    def fechar(self):
        self._aberta = False