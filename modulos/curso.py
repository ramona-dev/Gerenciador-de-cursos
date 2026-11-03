"""Representa um curso e valida seus dados acadêmicos."""


class Curso:
    def __init__(
        self,
        codigo: str,
        nome: str,
        carga_horaria: int,
        prerequisitos=None,
        ementa=None,
    ):
        self.codigo = codigo
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.prerequisitos = prerequisitos or []
        self.ementa = ementa

    @staticmethod
    def validar_codigo(valor):
        if not isinstance(valor, str):
            raise ValueError("Código do curso deve ser um texto.")

        codigo = valor.strip().upper()
        if len(codigo) < 3:
            raise ValueError(
                "Código do curso deve possuir pelo menos 3 caracteres."
            )
        return codigo

    @staticmethod
    def validar_nome(valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Nome do curso não pode ser vazio.")

        nome = " ".join(valor.split())
        if not any(caractere.isalpha() for caractere in nome):
            raise ValueError(
                "Nome do curso deve conter pelo menos uma letra."
            )
        return nome

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = self.validar_codigo(valor)

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = self.validar_nome(valor)

    @property
    def carga_horaria(self):
        return self._carga_horaria

    @carga_horaria.setter
    def carga_horaria(self, valor):
        if (
            isinstance(valor, bool)
            or not isinstance(valor, int)
            or valor <= 0
        ):
            raise ValueError(
                "Carga horária deve ser um número inteiro positivo."
            )
        self._carga_horaria = valor

    @property
    def prerequisitos(self):
        return list(self._prerequisitos)

    @prerequisitos.setter
    def prerequisitos(self, valor):
        if not isinstance(valor, list):
            raise TypeError("Pré-requisitos devem ser uma lista.")

        normalizados = []
        for codigo in valor:
            codigo = self.validar_codigo(codigo)
            if codigo == self.codigo:
                raise ValueError(
                    "Curso não pode ser pré-requisito de si mesmo."
                )
            if codigo in normalizados:
                raise ValueError("Pré-requisito repetido.")
            normalizados.append(codigo)

        self._prerequisitos = normalizados

    @property
    def ementa(self):
        return self._ementa

    @ementa.setter
    def ementa(self, valor):
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            self._ementa = None
            return
        if not isinstance(valor, str):
            raise ValueError("Ementa deve ser um texto ou ficar vazia.")
        self._ementa = " ".join(valor.split())

    def adicionar_prerequisito(self, codigo_pre: str):
        codigo_pre = self.validar_codigo(codigo_pre)
        if codigo_pre == self.codigo:
            raise ValueError(
                "Curso não pode ser pré-requisito de si mesmo."
            )
        if codigo_pre in self._prerequisitos:
            raise ValueError("Pré-requisito já cadastrado.")
        self._prerequisitos.append(codigo_pre)

    def remover_prerequisito(self, codigo_pre: str):
        codigo_pre = self.validar_codigo(codigo_pre)
        if codigo_pre not in self._prerequisitos:
            raise ValueError("Pré-requisito não encontrado.")
        self._prerequisitos.remove(codigo_pre)

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "carga_horaria": self.carga_horaria,
            "prerequisitos": self.prerequisitos,
            "ementa": self.ementa,
        }

    @classmethod
    def from_dict(cls, dados: dict):
        return cls(
            codigo=dados["codigo"],
            nome=dados["nome"],
            carga_horaria=int(dados["carga_horaria"]),
            prerequisitos=dados.get("prerequisitos", []),
            ementa=dados.get("ementa"),
        )

    def __str__(self):
        return (
            f"{self.codigo} - {self.nome} "
            f"({self.carga_horaria}h)"
        )

    def __repr__(self):
        return f"Curso({self.codigo!r}, {self.nome!r})"
