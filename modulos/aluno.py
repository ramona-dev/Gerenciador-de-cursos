"""Entidade Aluno, com histórico acadêmico e turmas ativas."""

from modulos.historico_academico import HistoricoAcademico
from modulos.pessoa import Pessoa


class Aluno(Pessoa, HistoricoAcademico):
    def __init__(self, matricula: str, nome: str, email: str):
        super().__init__(nome, email)

        if not isinstance(matricula, str) or not matricula.strip():
            raise ValueError("Matrícula não pode ser vazia.")

        self._matricula = matricula.strip()
        self._historico = []
        self._turmas = []

    @property
    def matricula(self):
        return self._matricula

    @property
    def turmas(self):
        return list(self._turmas)

    def adicionar_turma(self, turma):
        if turma not in self._turmas:
            self._turmas.append(turma)

    def remover_turma(self, turma):
        if turma in self._turmas:
            self._turmas.remove(turma)

    def to_dict(self):
        return {
            "matricula": self.matricula,
            "nome": self.nome,
            "email": self.email,
            "historico": self.historico,
        }

    @classmethod
    def from_dict(cls, dados: dict):
        aluno = cls(
            matricula=dados["matricula"],
            nome=dados["nome"],
            email=dados["email"],
        )

        historico = dados.get("historico", [])

        if not isinstance(historico, list):
            raise ValueError(
                f"Histórico inválido para o aluno {aluno.matricula}."
            )

        for item in historico:
            if not isinstance(item, dict) or "curso" not in item:
                raise ValueError(
                    f"Registro de histórico inválido para "
                    f"{aluno.matricula}."
                )

        aluno._historico = [
            dict(item)
            for item in historico
        ]

        return aluno

    def __lt__(self, other):
        if not isinstance(other, Aluno):
            return NotImplemented

        if self.cr == other.cr:
            return self.nome.casefold() < other.nome.casefold()

        return self.cr < other.cr

    def __repr__(self):
        return f"Aluno({self.matricula!r}, {self.nome!r})"