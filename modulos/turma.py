"""Turmas, horários e validações para matrícula."""

import re
from .oferta import Oferta

DIAS_VALIDOS = {"seg", "ter", "qua", "qui", "sex", "sab", "dom"}


def parse_horario(horario: str):
    """Converte HH:MM-HH:MM em minutos; rejeita horários impossíveis."""
    if not isinstance(horario, str):
        raise ValueError("Horário deve estar no formato HH:MM-HH:MM.")
    correspondencia = re.fullmatch(
        r"\s*(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})\s*",
        horario,
    )
    if not correspondencia:
        raise ValueError(
            f"Horário inválido: {horario!r}. Use o formato HH:MM-HH:MM."
        )
    h_inicio, m_inicio, h_fim, m_fim = map(int, correspondencia.groups())
    if h_inicio > 23 or h_fim > 23 or m_inicio > 59 or m_fim > 59:
        raise ValueError("Horário contém hora ou minuto fora do intervalo válido.")
    inicio = h_inicio * 60 + m_inicio
    fim = h_fim * 60 + m_fim
    if fim <= inicio:
        raise ValueError("O horário final deve ser posterior ao horário inicial.")
    return inicio, fim


def normalizar_dias(chave_dia):
    """Aceita 'seg qua', 'seg,qua' e transforma em dias individuais."""
    if not isinstance(chave_dia, str):
        raise ValueError("Dia da semana inválido.")
    dias = [parte.lower() for parte in re.split(r"[,;\s]+", chave_dia.strip()) if parte]
    if not dias:
        raise ValueError("Informe ao menos um dia da semana.")
    invalidos = [dia for dia in dias if dia not in DIAS_VALIDOS]
    if invalidos:
        raise ValueError(
            "Dia(s) inválido(s): " + ", ".join(invalidos)
            + ". Use seg, ter, qua, qui, sex, sab ou dom."
        )
    return list(dict.fromkeys(dias))


class Turma(Oferta):
    def __init__(self, curso, id_turma: str, semestre: str,
                 dias_horarios: dict, vagas: int, local: str = ""):
        if curso is None or not getattr(curso, "codigo", None):
            raise ValueError("A turma precisa estar vinculada a um curso válido.")
        super().__init__(semestre, vagas, local)
        if not isinstance(id_turma, str) or not id_turma.strip():
            raise ValueError("ID da turma não pode ser vazio.")
        self._curso = curso
        self._id = id_turma.strip().upper()
        self._matriculas = {}
        self._horarios = {}

        if not isinstance(dias_horarios, dict) or not dias_horarios:
            raise ValueError("Informe ao menos um dia e horário para a turma.")

        for chave_dia, valor in dias_horarios.items():
            dias = normalizar_dias(chave_dia)
            if isinstance(valor, str):
                valores = [valor]
            elif isinstance(valor, list) and valor:
                valores = valor
            else:
                raise ValueError(f"Formato inválido de horário para {chave_dia}.")

            intervalos = [parse_horario(item) for item in valores]
            for i, (inicio, fim) in enumerate(intervalos):
                for inicio2, fim2 in intervalos[i + 1:]:
                    if not (fim <= inicio2 or fim2 <= inicio):
                        raise ValueError(f"Há horários sobrepostos no dia {chave_dia}.")

            for dia in dias:
                if dia in self._horarios:
                    raise ValueError(f"Dia {dia} foi informado mais de uma vez.")
                self._horarios[dia] = list(intervalos)

    @property
    def curso(self):
        return self._curso

    @property
    def id(self):
        return self._id

    @property
    def horarios(self):
        return {dia: list(intervalos) for dia, intervalos in self._horarios.items()}

    @property
    def matriculas(self):
        return list(self._matriculas.values())

    def registrar_matricula(self, matricula):
        self._matriculas[matricula.aluno] = matricula

    def __len__(self):
        return sum(
            1 for matricula in self._matriculas.values()
            if matricula is not None and getattr(matricula, "ativa", False)
        )

    def tem_choque(self, outra_turma):
        if self.semestre != outra_turma.semestre:
            return False
        outros_horarios = outra_turma.horarios
        for dia, intervalos in self._horarios.items():
            if dia not in outros_horarios:
                continue
            for inicio, fim in intervalos:
                for inicio2, fim2 in outros_horarios[dia]:
                    if not (fim <= inicio2 or fim2 <= inicio):
                        return True
        return False

    def adicionar_aluno(self, aluno, configuracoes):
        if not self.aberta:
            raise ValueError("Turma está fechada.")

        matricula_existente = self._matriculas.get(aluno)
        if matricula_existente is not None and getattr(matricula_existente, "ativa", False):
            raise ValueError("Aluno já possui matrícula ativa nesta turma.")

        limite = configuracoes.get("max_turmas_por_aluno")
        if len(self) >= self.vagas:
            raise ValueError("Turma está lotada.")
        if limite is not None and len(aluno.turmas) >= int(limite):
            raise ValueError("Aluno já atingiu o limite de turmas.")

        for prerequisito in self.curso.prerequisitos:
            if not aluno.aprovado_em(prerequisito):
                raise ValueError(
                    f"Aluno não cumpriu o pré-requisito {prerequisito}."
                )

        for turma_existente in aluno.turmas:
            if self.tem_choque(turma_existente):
                raise ValueError(
                    f"Choque de horário com a turma {turma_existente.id}."
                )

    def _horarios_para_json(self):
        resultado = {}
        for dia, intervalos in self._horarios.items():
            resultado[dia] = []
            for inicio, fim in intervalos:
                h_inicio, m_inicio = divmod(inicio, 60)
                h_fim, m_fim = divmod(fim, 60)
                resultado[dia].append(
                    f"{h_inicio:02d}:{m_inicio:02d}-{h_fim:02d}:{m_fim:02d}"
                )
        return resultado

    def to_dict(self):
        return {
            "id": self.id,
            "curso": self.curso.codigo,
            "semestre": self.semestre,
            "horarios": self._horarios_para_json(),
            "vagas": self.vagas,
            "local": self.local,
            "aberta": self.aberta,
        }

    @classmethod
    def from_dict(cls, dados: dict, curso):
        turma = cls(
            curso=curso,
            id_turma=dados["id"],
            semestre=dados["semestre"],
            dias_horarios=dados["horarios"],
            vagas=int(dados["vagas"]),
            local=dados.get("local", ""),
        )
        turma._aberta = bool(dados.get("aberta", True))
        return turma
