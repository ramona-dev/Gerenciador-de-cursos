"""Classe-base para pessoas cadastradas no sistema."""

import re


class Pessoa:
    def __init__(self, nome: str, email: str):
        self.nome = nome
        self.email = email

    @staticmethod
    def validar_nome(valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Nome não pode ser vazio.")

        nome = " ".join(valor.split())
        if not any(caractere.isalpha() for caractere in nome):
            raise ValueError("Nome deve conter pelo menos uma letra.")
        if any(caractere.isdigit() for caractere in nome):
            raise ValueError("Nome de pessoa não pode conter números.")
        return nome

    @staticmethod
    def validar_email(valor):
        if not isinstance(valor, str):
            raise ValueError("E-mail deve ser um texto.")

        email = valor.strip()
        padrao = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        if not re.fullmatch(padrao, email):
            raise ValueError(
                "E-mail inválido. Informe um endereço no formato nome@dominio.com."
            )
        return email

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = self.validar_nome(valor)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        self._email = self.validar_email(valor)
