from .oferta import Oferta

def parse_horario(h: str):
    """Converte '08:00-10:00' em tupla (480, 600) de minutos."""
    ini, fim = h.split("-")
    h_ini, m_ini = map(int, ini.split(":"))
    h_fim, m_fim = map(int, fim.split(":"))
    return h_ini * 60 + m_ini, h_fim * 60 + m_fim

class Turma(Oferta):
    def __init__(self, curso, id_turma: str, semestre: str, dias_horarios: dict, vagas: int, local: str = ""):
        super().__init__(semestre, vagas, local)
        self._curso = curso
        self._id = id_turma
        self._matriculas = {}

        # 🚀 Correção: aceita string ou lista de strings
        self._horarios = {}
        for dia, val in (dias_horarios or {}).items():
            if isinstance(val, str):
                self._horarios[dia] = [parse_horario(val)]
            elif isinstance(val, list):
                self._horarios[dia] = [parse_horario(v) for v in val if isinstance(v, str)]
            else:
                raise ValueError(f"Formato inválido de horário para {dia}: {val}")

    @property
    def curso(self): return self._curso
    @property
    def id(self): return self._id
    @property
    def horarios(self): return {d: list(v) for d, v in self._horarios.items()}

    def __len__(self):
        return sum(1 for m in self._matriculas.values() if m and m.ativa)

    def tem_choque(self, outra_turma):
        for dia, intervalos in self._horarios.items():
            if dia in outra_turma._horarios:
                for (ini, fim) in intervalos:
                    for (ini2, fim2) in outra_turma._horarios[dia]:
                        if not (fim <= ini2 or fim2 <= ini):
                            return True
        return False

    def adicionar_aluno(self, aluno, settings):
        if not self.aberta:
            raise ValueError("Turma está fechada.")
        if len(self) >= self.vagas:
            raise ValueError("Turma está lotada.")
        if settings.get("max_turmas_por_aluno") and len(aluno.turmas) >= settings["max_turmas_por_aluno"]:
            raise ValueError("Aluno já atingiu o limite de turmas.")
        for prereq in self.curso.prerequisitos:
            if not aluno.aprovado_em(prereq):
                raise ValueError(f"Aluno não cumpriu o pré-requisito {prereq}.")
        for t in aluno.turmas:
            if self.tem_choque(t):
                raise ValueError(f"Choque de horário com a turma {t.id}.")
        self._matriculas[aluno] = None  # será preenchido pela Matricula