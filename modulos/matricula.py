"""Vínculo acadêmico entre um aluno e uma turma."""

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

    def lancar_nota(self, nota: float):
        self._validar_ativa("lançar nota")
        nota = float(nota)
        if not 0 <= nota <= 10:
            raise ValueError("Nota deve estar entre 0 e 10.")
        self._nota = nota

    def lancar_frequencia(self, frequencia: float):
        self._validar_ativa("lançar frequência")
        frequencia = float(frequencia)
        if not 0 <= frequencia <= 100:
            raise ValueError("Frequência deve estar entre 0 e 100.")
        self._frequencia = frequencia

    def trancar(self, configuracoes):
        if not self._ativa:
            raise ValueError("Matrícula já está trancada.")
        limite = configuracoes.get("data_limite_trancamento")
        if isinstance(limite, str):
            limite = date.fromisoformat(limite)
        if not isinstance(limite, date):
            raise ValueError("Data limite de trancamento inválida.")
        if date.today() > limite:
            raise ValueError("Data limite de trancamento já passou.")
        self._ativa = False
        self._aluno.remover_turma(self._turma)

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
        matricula = cls.__new__(cls)
        matricula._aluno = aluno
        matricula._turma = turma
        matricula._nota = dados.get("nota")
        matricula._frequencia = dados.get("frequencia")
        matricula._ativa = bool(dados.get("ativa", True))
        matricula._data = date.fromisoformat(dados["data"])

        if matricula._nota is not None and not 0 <= float(matricula._nota) <= 10:
            raise ValueError("Matrícula contém nota fora do intervalo de 0 a 10.")
        if matricula._frequencia is not None and not 0 <= float(matricula._frequencia) <= 100:
            raise ValueError("Matrícula contém frequência fora do intervalo de 0 a 100.")

        # Matrículas trancadas continuam no histórico da turma, mas não ocupam
        # vaga nem devem gerar choque/limite de turmas para o aluno.
        if matricula._ativa:
            aluno.adicionar_turma(turma)
        turma.registrar_matricula(matricula)
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
