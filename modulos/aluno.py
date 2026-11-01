from .pessoa import Pessoa


class Aluno(Pessoa):

    def __init__(
        self,
        matricula: str,
        nome: str,
        email: str
    ):
        super().__init__(
            nome,
            email
        )

        if not matricula.strip():
            raise ValueError(
                "Matrícula não pode ser vazia."
            )

        self._matricula = matricula
        self._historico = []
        self._turmas = []

    @property
    def matricula(self):
        return self._matricula

    @property
    def historico(self):
        return list(self._historico)

    @property
    def turmas(self):
        return list(self._turmas)

    @property
    def cr(self):

        if not self._historico:
            return 0.0

        return sum(
            disciplina["nota"]
            for disciplina in self._historico
        ) / len(self._historico)

    def adicionar_disciplina(
        self,
        curso,
        nota,
        frequencia
    ):

        self._historico.append({
            "curso": curso.codigo,
            "nota": nota,
            "frequencia": frequencia
        })

    def adicionar_turma(
        self,
        turma
    ):

        if turma not in self._turmas:
            self._turmas.append(
                turma
            )

    def remover_turma(
        self,
        turma
    ):

        if turma in self._turmas:
            self._turmas.remove(
                turma
            )

    def aprovado_em(
        self,
        codigo_curso
    ):

        return any(
            disciplina["curso"] == codigo_curso
            and disciplina["nota"] >= 6
            and disciplina["frequencia"] >= 75
            for disciplina in self._historico
        )

    def to_dict(self):

        return {
            "matricula": self.matricula,
            "nome": self.nome,
            "email": self.email,
            "historico": self.historico
        }

    @classmethod
    def from_dict(
        cls,
        dados: dict
    ):

        aluno = cls(
            matricula=dados["matricula"],
            nome=dados["nome"],
            email=dados["email"]
        )

        aluno._historico = dados.get(
            "historico",
            []
        )

        return aluno

    def __lt__(
        self,
        other
    ):

        if self.cr == other.cr:
            return (
                self.nome
                <
                other.nome
            )

        return self.cr < other.cr

    def __repr__(self):

        return (
            f"Aluno("
            f"{self.matricula}, "
            f"{self.nome})"
        )