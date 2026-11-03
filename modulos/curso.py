"""Representa um curso e suas regras básicas."""


class Curso:
    def __init__(self, codigo: str, nome: str, carga_horaria: int, prerequisitos=None):
        self.codigo = codigo
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.prerequisitos = prerequisitos or []

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ValueError("Código do curso deve possuir pelo menos 3 caracteres.")
        self._codigo = valor.strip().upper()

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Nome do curso não pode ser vazio.")
        self._nome = valor.strip()

    @property
    def carga_horaria(self):
        return self._carga_horaria

    @carga_horaria.setter
    def carga_horaria(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise ValueError("Carga horária deve ser um número inteiro positivo.")
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
            if not isinstance(codigo, str) or len(codigo.strip()) < 3:
                raise ValueError("Código de pré-requisito inválido.")
            codigo = codigo.strip().upper()
            if codigo == self.codigo:
                raise ValueError("Curso não pode ser pré-requisito de si mesmo.")
            if codigo in normalizados:
                raise ValueError("Pré-requisito repetido.")
            normalizados.append(codigo)
        self._prerequisitos = normalizados

    def adicionar_prerequisito(self, codigo_pre: str):
        codigo_pre = codigo_pre.strip().upper()
        if codigo_pre == self.codigo:
            raise ValueError("Curso não pode ser pré-requisito de si mesmo.")
        if codigo_pre in self._prerequisitos:
            raise ValueError("Pré-requisito já cadastrado.")
        self._prerequisitos.append(codigo_pre)

    def remover_prerequisito(self, codigo_pre: str):
        codigo_pre = codigo_pre.strip().upper()
        if codigo_pre not in self._prerequisitos:
            raise ValueError("Pré-requisito não encontrado.")
        self._prerequisitos.remove(codigo_pre)

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "carga_horaria": self.carga_horaria,
            "prerequisitos": self.prerequisitos,
        }

    @classmethod
    def from_dict(cls, dados: dict):
        return cls(
            codigo=dados["codigo"],
            nome=dados["nome"],
            carga_horaria=int(dados["carga_horaria"]),
            prerequisitos=dados.get("prerequisitos", []),
        )

    def __str__(self):
        return f"{self.codigo} - {self.nome} ({self.carga_horaria}h)"

    def __repr__(self):
        return f"Curso({self.codigo!r}, {self.nome!r})"
