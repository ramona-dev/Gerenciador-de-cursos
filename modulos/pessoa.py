" Validações: Nome e email não podem ser vazios."

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
    
    @nome.setter
    def nome(self, valor):

     if not valor.strip():
        raise ValueError(
            "Nome não pode ser vazio."
        )
     self._nome = valor
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, valor):
        if "@" not in valor:
            raise ValueError(
                "Email inválido."
            )
        self._email = valor