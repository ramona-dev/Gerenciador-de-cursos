"""Vínculo acadêmico entre um aluno e uma turma."""

import math
from datetime import date
import settings


class Matricula:
    def __init__(self, aluno, turma):
        configuracoes = settings.obter_configuracoes()
        turma.adicionar_aluno(aluno, configuracoes)
        self._aluno = aluno
        self._turma = turma
        self._nota = None
        self._frequencia = None
        self._ativa = True
        self._data = date.today()
        aluno.adicionar_turma(turma)
        turma.registrar_matricula(self)

    @property
    def aluno(self):
        return self._aluno

    @property
    def turma(self):
        return self._turma

    @property
    def nota(self):
        return self._nota

    @property
    def frequencia(self):
        return self._frequencia

    @property
    def ativa(self):
        return self._ativa

    @property
    def data(self):
        return self._data

    def _validar_ativa(self, operacao):
        if not self._ativa:
            raise ValueError(
                f"Não é possível {operacao} em uma matrícula trancada."
            )

    @staticmethod
    def _validar_numero(valor, campo, minimo, maximo):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError(f"{campo} deve ser numérico.")
        numero = float(valor)
        if not math.isfinite(numero) or not minimo <= numero <= maximo:
            raise ValueError(f"{campo} deve estar entre {minimo} e {maximo}.")
        return numero

    def _sincronizar_historico(self):
        if not self._ativa:
            self._aluno.remover_resultado_matricula(self._turma.id)
        elif self._nota is not None and self._frequencia is not None:
            self._aluno.registrar_resultado_matricula(
                self._turma.curso.codigo,
                self._nota,
                self._frequencia,
                self._turma.id,
            )

    def lancar_nota(self, nota: float):
        self._validar_ativa("lançar nota")
        self._nota = self._validar_numero(nota, "Nota", 0, 10)
        self._sincronizar_historico()

    def lancar_frequencia(self, frequencia: float):
        self._validar_ativa("lançar frequência")
        self._frequencia = self._validar_numero(
            frequencia, "Frequência", 0, 100
        )
        self._sincronizar_historico()

    def trancar(self, configuracoes):
        if not self._ativa:
            raise ValueError("Matrícula já está trancada.")
        limite = configuracoes.get("data_limite_trancamento")
        if isinstance(limite, str):
            try:
                limite = date.fromisoformat(limite)
            except ValueError as erro:
                raise ValueError("Data limite de trancamento inválida.") from erro
        if not isinstance(limite, date):
            raise ValueError("Data limite de trancamento inválida.")
        if date.today() > limite:
            raise ValueError("Data limite de trancamento já passou.")
        self._ativa = False
        self._aluno.remover_turma(self._turma)
        self._sincronizar_historico()

    def situacao(self):
        if not self._ativa:
            return "TRANCADA"
        if self._nota is None or self._frequencia is None:
            return "CURSANDO"
        if self._nota < settings.nota_minima_aprovacao:
            return "REPROVADO_POR_NOTA"
        if self._frequencia < settings.frequencia_minima:
            return "REPROVADO_POR_FREQUENCIA"
        return "APROVADO"

    def to_dict(self):
        return {
            "aluno": self.aluno.matricula,
            "turma": self.turma.id,
            "nota": self.nota,
            "frequencia": self.frequencia,
            "ativa": self.ativa,
            "data": self.data.isoformat(),
        }

    @classmethod
    def from_dict(cls, dados, aluno, turma):
        if not isinstance(dados, dict):
            raise ValueError("Registro de matrícula deve ser um objeto JSON.")

        ativa = dados.get("ativa", True)
        if not isinstance(ativa, bool):
            raise ValueError("O campo 'ativa' da matrícula deve ser booleano.")

        nota = dados.get("nota")
        frequencia = dados.get("frequencia")
        if nota is not None:
            nota = cls._validar_numero(nota, "Nota da matrícula", 0, 10)
        if frequencia is not None:
            frequencia = cls._validar_numero(
                frequencia, "Frequência da matrícula", 0, 100
            )

        if not isinstance(dados.get("data"), str):
            raise ValueError("Data da matrícula deve estar no formato AAAA-MM-DD.")
        try:
            data_matricula = date.fromisoformat(dados["data"])
        except ValueError as erro:
            raise ValueError("Data da matrícula inválida. Use AAAA-MM-DD.") from erro

        matricula = cls.__new__(cls)
        matricula._aluno = aluno
        matricula._turma = turma
        matricula._nota = nota
        matricula._frequencia = frequencia
        matricula._ativa = ativa
        matricula._data = data_matricula

        # Registros trancados permanecem no histórico da turma, mas não ocupam
        # vaga, não aparecem nas turmas ativas do aluno e não contam no CR.
        if ativa:
            aluno.adicionar_turma(turma)
        turma.registrar_matricula(matricula)
        matricula._sincronizar_historico()
        return matricula

    def __eq__(self, other):
        if not isinstance(other, Matricula):
            return False
        return (
            self.aluno.matricula == other.aluno.matricula
            and self.turma.id == other.turma.id
        )

    def __repr__(self):
        return f"Matricula({self.aluno.matricula!r}, {self.turma.id!r})"
