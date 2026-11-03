"""Responsabilidades relacionadas ao histórico acadêmico de um aluno."""

import settings


class HistoricoAcademico:
    """Componente reutilizável para gerenciamento do histórico acadêmico."""

    @property
    def historico(self):
        return [dict(item) for item in self._historico]

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
            raise ValueError(
                "Nota do histórico deve estar entre 0 e 10."
            )

        if not 0 <= float(frequencia) <= 100:
            raise ValueError(
                "Frequência do histórico deve estar entre 0 e 100."
            )

        codigo = getattr(curso, "codigo", curso)

        if not codigo:
            raise ValueError(
                "Curso do histórico inválido."
            )

        self._historico.append(
            {
                "curso": str(codigo).strip().upper(),
                "nota": float(nota),
                "frequencia": float(frequencia),
            }
        )

    def aprovado_em(self, codigo_curso):
        codigo_curso = str(codigo_curso).strip().upper()

        return any(
            str(item.get("curso", "")).strip().upper()
            == codigo_curso
            and item.get("nota") is not None
            and item.get("frequencia") is not None
            and float(item["nota"])
            >= settings.nota_minima_aprovacao
            and float(item["frequencia"])
            >= settings.frequencia_minima
            for item in self._historico
        )