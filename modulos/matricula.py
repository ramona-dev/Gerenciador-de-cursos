from datetime import date

import settings


class Matricula:

    def __init__(self, aluno, turma):

        turma.adicionar_aluno(
            aluno,
            settings.__dict__
        )

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

    def lancar_nota(self, nota: float):

        if not 0 <= nota <= 10:
            raise ValueError(
                "Nota deve estar entre 0 e 10."
            )

        self._nota = nota

    def lancar_frequencia(
        self,
        frequencia: float
    ):

        if not 0 <= frequencia <= 100:
            raise ValueError(
                "Frequência deve estar entre 0 e 100."
            )

        self._frequencia = frequencia

    def trancar(self, settings_dict):

        if (
            str(date.today())
            >
            settings_dict[
                "data_limite_trancamento"
            ]
        ):
            raise ValueError(
                "Data limite de trancamento já passou."
            )

        self._ativa = False

        self._aluno.remover_turma(
            self._turma
        )

    def situacao(self):

        if not self._ativa:
            return "TRANCADA"

        if (
            self._nota is None
            or
            self._frequencia is None
        ):
            return "CURSANDO"

        if (
            self._nota
            <
            settings.nota_minima_aprovacao
        ):
            return "REPROVADO_POR_NOTA"

        if (
            self._frequencia
            <
            settings.frequencia_minima
        ):
            return "REPROVADO_POR_FREQUENCIA"

        return "APROVADO"

    def __eq__(self, other):

        if not isinstance(
            other,
            Matricula
        ):
            return False

        return (
            self.aluno.matricula
            ==
            other.aluno.matricula
            and
            self.turma.id
            ==
            other.turma.id
        )

    def __repr__(self):

        return (
            f"Matricula("
            f"{self.aluno.matricula}, "
            f"{self.turma.id})"
        )