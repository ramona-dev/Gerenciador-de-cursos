"""Classe-base para pessoas cadastradas no sistema."""


class Pessoa:
    def __init__(self, nome: str, email: str):
        self.nome = nome
        self.email = email

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Nome não pode ser vazio.")
        self._nome = valor.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if not isinstance(valor, str) or "@" not in valor.strip():
            raise ValueError("Email inválido.")
        self._email = valor.strip()
