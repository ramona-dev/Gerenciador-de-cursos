from .oferta import Oferta

class Turma(Oferta):
    def __init__(self, curso, id_turma: str, semestre: str, dias_horario: dict, vagas: int, local: str = ""):
        super().__init__(semestre, vagas, local)
        self._curso = curso
        self._id = id_turma
        self._matriculas = {}
    
    def curso(self):
        pass
    
    def id(self):
        pass
    
    def horarios(self):
        pass

    def tem_choque(self):
        pass

    def adicionar_aluno(self):
        pass