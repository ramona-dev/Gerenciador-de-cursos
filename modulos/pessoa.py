class Pessoa:
    def __init__(self, nome: str, email: str):
        if not nome.strip():
            raise ValueError("Nome não pode ser vazio.")
        if "@" not in email:
            raise ValueError("Email inválido.")
        self._nome = nome
        self._email = email

    @property
    def nome(self):
        return self._nome

    @property
    def email(self):
        return self._email