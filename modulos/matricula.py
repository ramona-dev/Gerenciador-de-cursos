from datetime import date
import settings

class Matricula:
    def __init__(self, aluno, turma):
        # chama o método da Turma para validar regras e registrar
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
        pass

    def lancar_frequencia(self, freq: float):
        pass

    def trancar(self, settings):
       pass

    def situacao(self):
       pass