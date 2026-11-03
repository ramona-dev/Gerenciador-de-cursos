"""Dados comuns às ofertas de disciplinas, como semestre e capacidade."""

import re


class Oferta:
    def __init__(self, semestre: str, vagas: int, local: str = ""):
        self.semestre = semestre
        self.vagas = vagas
        self.local = local
        self._aberta = True

    @staticmethod
    def validar_semestre(valor):
        if not isinstance(valor, str):
            raise ValueError("Semestre deve estar no formato AAAA.1 ou AAAA.2.")

        semestre = valor.strip()
        if not re.fullmatch(r"\d{4}\.[12]", semestre):
            raise ValueError(
                "Semestre inválido. Use o formato AAAA.1 ou AAAA.2, por exemplo 2026.2."
            )
        return semestre

    @property
    def semestre(self):
        return self._semestre

    @semestre.setter
    def semestre(self, valor):
        self._semestre = self.validar_semestre(valor)

    @property
    def vagas(self):
        return self._vagas

    @vagas.setter
    def vagas(self, valor: int):
        if (
            isinstance(valor, bool)
            or not isinstance(valor, int)
            or valor <= 0
        ):
            raise ValueError(
                "Número de vagas deve ser um número inteiro positivo."
            )
        self._vagas = valor

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, valor):
        if valor is None:
            valor = ""
        if not isinstance(valor, str):
            raise ValueError("Local deve ser um texto.")
        self._local = valor.strip()

    @property
    def aberta(self):
        return self._aberta

    def abrir(self):
        self._aberta = True

    def fechar(self):
        self._aberta = False
