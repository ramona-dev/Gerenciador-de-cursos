from .oferta import Oferta


def parse_horario(horario: str):

    inicio, fim = horario.split("-")

    h_inicio, m_inicio = map(
        int,
        inicio.split(":")
    )

    h_fim, m_fim = map(
        int,
        fim.split(":")
    )

    return (
        h_inicio * 60 + m_inicio,
        h_fim * 60 + m_fim
    )


class Turma(Oferta):

    def __init__(
        self,
        curso,
        id_turma: str,
        semestre: str,
        dias_horarios: dict,
        vagas: int,
        local: str = ""
    ):

        super().__init__(
            semestre,
            vagas,
            local
        )

        self._curso = curso
        self._id = id_turma
        self._matriculas = {}

        self._horarios = {}

        for dia, valor in (
            dias_horarios or {}
        ).items():

            if isinstance(
                valor,
                str
            ):

                self._horarios[dia] = [
                    parse_horario(valor)
                ]

            elif isinstance(
                valor,
                list
            ):

                self._horarios[dia] = [
                    parse_horario(v)
                    for v in valor
                ]

            else:
                raise ValueError(
                    f"Formato inválido de horário para {dia}"
                )

    @property
    def curso(self):
        return self._curso

    @property
    def id(self):
        return self._id

    @property
    def horarios(self):

        return {
            dia: list(intervalos)
            for dia, intervalos
            in self._horarios.items()
        }

    @property
    def matriculas(self):
        return list(
            self._matriculas.values()
        )

    def registrar_matricula(
        self,
        matricula
    ):

        self._matriculas[
            matricula.aluno
        ] = matricula

    def __len__(self):

        return sum(
            1
            for matricula
            in self._matriculas.values()
            if (
                matricula
                and matricula.ativa
            )
        )

    def tem_choque(
        self,
        outra_turma
    ):

        for (
            dia,
            intervalos
        ) in self._horarios.items():

            if (
                dia
                not in outra_turma.horarios
            ):
                continue

            for (
                inicio,
                fim
            ) in intervalos:

                for (
                    inicio2,
                    fim2
                ) in outra_turma.horarios[dia]:

                    if not (
                        fim <= inicio2
                        or fim2 <= inicio
                    ):
                        return True

        return False

    def adicionar_aluno(
        self,
        aluno,
        settings
    ):

        if not self.aberta:
            raise ValueError(
                "Turma está fechada."
            )

        if len(self) >= self.vagas:
            raise ValueError(
                "Turma está lotada."
            )

        limite = settings.get(
            "max_turmas_por_aluno"
        )

        if (
            limite
            and len(aluno.turmas) >= limite
        ):
            raise ValueError(
                "Aluno já atingiu o limite de turmas."
            )

        for (
            prerequisito
        ) in self.curso.prerequisitos:

            if not aluno.aprovado_em(
                prerequisito
            ):
                raise ValueError(
                    f"Aluno não cumpriu o pré-requisito {prerequisito}."
                )

        for turma in aluno.turmas:

            if self.tem_choque(
                turma
            ):
                raise ValueError(
                    f"Choque de horário com a turma {turma.id}."
                )

    def _horarios_para_json(self):

        horarios = {}

        for (
            dia,
            intervalos
        ) in self._horarios.items():
            horarios[dia] = []

            for (
                inicio,
                fim
            ) in intervalos:

                h_inicio = inicio // 60
                m_inicio = inicio % 60

                h_fim = fim // 60
                m_fim = fim % 60

                horarios[dia].append(
                    f"{h_inicio:02}:{m_inicio:02}-{h_fim:02}:{m_fim:02}"
                )

        return horarios

    def to_dict(self):

        return {
            "id": self.id,
            "curso": self.curso.codigo,
            "semestre": self.semestre,
            "horarios": self._horarios_para_json(),
            "vagas": self.vagas,
            "local": self.local,
            "aberta": self.aberta
        }

    @classmethod
    def from_dict(
        cls,
        dados: dict,
        curso
    ):

        turma = cls(
            curso=curso,
            id_turma=dados["id"],
            semestre=dados["semestre"],
            dias_horarios=dados["horarios"],
            vagas=dados["vagas"],
            local=dados.get(
                "local",
                ""
            )
        )

        turma._aberta = dados.get(
            "aberta",
            True
        )

        return turma