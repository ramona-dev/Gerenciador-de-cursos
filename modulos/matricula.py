from datetime import date
import settings

class Matricula:
    def __init__(self, aluno, turma):
        # 🚀 chama o método da Turma para validar regras e registrar
        turma.adicionar_aluno(aluno, settings.__dict__)
        self._aluno = aluno
        self._turma = turma
        self._nota = None
        self._frequencia = None
        self._ativa = True
        self._data = date.today()

        # registra a matrícula dentro da turma
        turma._matriculas[aluno] = self

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
        self._ativa
    @property
    def data(self):
        return self._data

    def lancar_nota(self, nota: float):
        if nota < 0 or nota > 10:
            raise ValueError("Nota deve estar entre 0 e 10.")
        self._nota = nota

    def lancar_frequencia(self, freq: float):
        if freq < 0 or freq > 100:
            raise ValueError("Frequência deve estar entre 0 e 100.")
        self._frequencia = freq

    def trancar(self, settings):
        # respeita data limite
        if str(date.today()) > settings["data_limite_trancamento"]:
            raise ValueError("Data limite de trancamento já passou.")
        self._ativa = False

    def situacao(self):
        if not self._ativa:
            return "TRANCADA"
        if self._nota is None or self._frequencia is None:
            return "CURSANDO"
        if self._nota >= settings.nota_minima_aprovacao and self._frequencia >= settings.frequencia_minima:
            return "APROVADO"
        return "REPROVADO"