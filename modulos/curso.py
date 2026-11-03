
class Curso:

    def __init__(
        self,
        codigo: str,
        nome: str,
        carga_horaria: int,
        prerequisitos=None
    ):
        self.codigo = codigo
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.prerequisitos = prerequisitos or []

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):

        if not valor.strip():
            raise ValueError(
                "Nome do curso não pode ser vazio."
            )

        self._nome = valor

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):

        if (
            not valor
            or len(valor.strip()) < 3
        ):
            raise ValueError(
                "Código do curso deve possuir pelo menos 3 caracteres."
            )

        self._codigo = valor

    @property
    def carga_horaria(self):
        return self._carga_horaria

    @carga_horaria.setter
    def carga_horaria(self, valor):

        if valor <= 0:
            raise ValueError(
                "Carga horária deve ser positiva."
            )

        self._carga_horaria = valor

    @property
    def prerequisitos(self):
        return list(self._prerequisitos)

    @prerequisitos.setter
    def prerequisitos(self, valor):

        if not isinstance(valor, list):
            raise TypeError(
                "Pré-requisitos devem ser uma lista."
            )

        self._prerequisitos = list(valor)

    def adicionar_prerequisito(
        self,
        codigo_pre: str
    ):

        if codigo_pre == self.codigo:
            raise ValueError(
                "Curso não pode ser pré-requisito de si mesmo."
            )

        if codigo_pre in self._prerequisitos:
            raise ValueError(
                "Pré-requisito já cadastrado."
            )

        self._prerequisitos.append(
            codigo_pre
        )

    def to_dict(self):

        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "carga_horaria": self.carga_horaria,
            "prerequisitos": self.prerequisitos
        }

    @classmethod
    def from_dict(
        cls,
        dados: dict
    ):

        return cls(
            codigo=dados["codigo"],
            nome=dados["nome"],
            carga_horaria=dados["carga_horaria"],
            prerequisitos=dados.get(
                "prerequisitos",
                []
            )
        )

    def __str__(self):

        return (
            f"{self.codigo} - "
            f"{self.nome} "
            f"({self.carga_horaria}h)"
        )

    def __repr__(self):

        return (
            f"Curso("
            f"{self.codigo}, "
            f"{self.nome})"
        )


def test_impede_ciclo_de_prerequisitos():


    mat = Curso(
        "MAT101",
        "Matemática",
        60
    )

    alg = Curso(
        "ALG101",
        "Algoritmos",
        60
    )

    poo = Curso(
        "POO101",
        "POO",
        60
    )

    catalogo = CatalogoCursos(
        [mat, alg, poo]
    )

    catalogo.adicionar_prerequisito(
        "POO101",
        "ALG101"
    )

    catalogo.adicionar_prerequisito(
        "ALG101",
        "MAT101"
    )

    with pytest.raises(
        ValueError
    ):

        catalogo.adicionar_prerequisito(
            "MAT101",
            "POO101"
        )