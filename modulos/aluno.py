"""Entidade Aluno, com herança múltipla e histórico acadêmico."""

from modulos.historico_academico import HistoricoAcademico
from modulos.pessoa import Pessoa


class Aluno(Pessoa, HistoricoAcademico):
    def __init__(self, matricula: str, nome: str, email: str):
        super().__init__(nome, email)

        if not isinstance(matricula, str) or not matricula.strip():
            raise ValueError("Matrícula não pode ser vazia.")

        matricula = matricula.strip()
        if not matricula.isascii() or not matricula.isdecimal():
            raise ValueError(
                "Matrícula deve conter somente números (0 a 9)."
            )

        self._matricula = matricula
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
    def from_dict(cls, dados: dict, codigos_cursos=None):
        if not isinstance(dados, dict):
            raise ValueError("Registro de aluno deve ser um objeto JSON.")

        aluno = cls(
            matricula=dados["matricula"],
            nome=dados["nome"],
            email=dados["email"],
        )
        historico = dados.get("historico", [])
        if not isinstance(historico, list):
            raise ValueError(f"Histórico inválido para o aluno {aluno.matricula}.")

        turmas_registradas = set()
        for indice, item in enumerate(historico, start=1):
            if not isinstance(item, dict):
                raise ValueError(
                    f"Registro {indice} do histórico de {aluno.matricula} deve ser um objeto."
                )
            if not {"curso", "nota", "frequencia"}.issubset(item):
                raise ValueError(
                    f"Registro {indice} do histórico de {aluno.matricula} está incompleto."
                )

            codigo = item["curso"]
            if not isinstance(codigo, str) or len(codigo.strip()) < 3:
                raise ValueError(
                    f"Código de curso inválido no histórico de {aluno.matricula}."
                )
            codigo = codigo.strip().upper()
            if codigos_cursos is not None and codigo not in codigos_cursos:
                raise ValueError(
                    f"O histórico do aluno {aluno.matricula} referencia "
                    f"o curso inexistente {codigo}."
                )

            aluno.adicionar_disciplina(codigo, item["nota"], item["frequencia"])

            id_turma = item.get("turma")
            if id_turma is not None:
                if not isinstance(id_turma, str) or not id_turma.strip():
                    raise ValueError(
                        f"ID de turma inválido no histórico de {aluno.matricula}."
                    )
                id_turma = id_turma.strip().upper()
                if id_turma in turmas_registradas:
                    raise ValueError(
                        f"Histórico de {aluno.matricula} possui resultado duplicado "
                        f"para a turma {id_turma}."
                    )
                turmas_registradas.add(id_turma)
                aluno._historico[-1]["turma"] = id_turma

        return aluno

    def __lt__(self, other):
        if not isinstance(other, Aluno):
            return NotImplemented
        if self.cr == other.cr:
            return self.nome.casefold() < other.nome.casefold()
        return self.cr < other.cr

    def __repr__(self):
        return f"Aluno({self.matricula!r}, {self.nome!r})"
