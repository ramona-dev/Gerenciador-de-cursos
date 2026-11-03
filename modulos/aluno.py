"""Entidade Aluno, com histórico acadêmico e turmas ativas."""

import settings
from modulos.pessoa import Pessoa


class Aluno(Pessoa):
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
    def historico(self):
        return [dict(item) for item in self._historico]

    @property
    def turmas(self):
        return list(self._turmas)

    @property
    def cr(self):
        notas = [
            float(item["nota"])
            for item in self._historico
            if item.get("nota") is not None
        ]
        return sum(notas) / len(notas) if notas else 0.0

    def calculo_de_CR(self):
        return self.cr

    def adicionar_disciplina(self, curso, nota, frequencia):
        if not 0 <= float(nota) <= 10:
            raise ValueError("Nota do histórico deve estar entre 0 e 10.")
        if not 0 <= float(frequencia) <= 100:
            raise ValueError("Frequência do histórico deve estar entre 0 e 100.")
        codigo = getattr(curso, "codigo", curso)
        if not codigo:
            raise ValueError("Curso do histórico inválido.")
        self._historico.append({
            "curso": str(codigo).strip().upper(),
            "nota": float(nota),
            "frequencia": float(frequencia),
        })

    def adicionar_turma(self, turma):
        if turma not in self._turmas:
            self._turmas.append(turma)

    def remover_turma(self, turma):
        if turma in self._turmas:
            self._turmas.remove(turma)

    def aprovado_em(self, codigo_curso):
        codigo_curso = str(codigo_curso).strip().upper()
        return any(
            str(item.get("curso", "")).strip().upper() == codigo_curso
            and item.get("nota") is not None
            and item.get("frequencia") is not None
            and float(item["nota"]) >= settings.nota_minima_aprovacao
            and float(item["frequencia"]) >= settings.frequencia_minima
            for item in self._historico
        )

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
            raise ValueError(f"Histórico inválido para o aluno {aluno.matricula}.")
        for item in historico:
            if not isinstance(item, dict) or "curso" not in item:
                raise ValueError(f"Registro de histórico inválido para {aluno.matricula}.")
        aluno._historico = [dict(item) for item in historico]
        return aluno

    def __lt__(self, other):
        if not isinstance(other, Aluno):
            return NotImplemented
        if self.cr == other.cr:
            return self.nome.casefold() < other.nome.casefold()
        return self.cr < other.cr

    def __repr__(self):
        return f"Aluno({self.matricula!r}, {self.nome!r})"
