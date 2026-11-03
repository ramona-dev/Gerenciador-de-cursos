"""Responsabilidades relacionadas ao histórico acadêmico de um aluno."""

import math
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

    @staticmethod
    def _validar_numero(valor, campo, minimo, maximo):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError(f"{campo} deve ser numérico.")
        numero = float(valor)
        if not math.isfinite(numero) or not minimo <= numero <= maximo:
            raise ValueError(f"{campo} deve estar entre {minimo} e {maximo}.")
        return numero

    @staticmethod
    def _normalizar_codigo(curso):
        codigo = getattr(curso, "codigo", curso)
        if not isinstance(codigo, str) or len(codigo.strip()) < 3:
            raise ValueError("Curso do histórico inválido.")
        return codigo.strip().upper()

    def adicionar_disciplina(self, curso, nota, frequencia):
        codigo = self._normalizar_codigo(curso)
        nota = self._validar_numero(nota, "Nota do histórico", 0, 10)
        frequencia = self._validar_numero(
            frequencia, "Frequência do histórico", 0, 100
        )
        self._historico.append({
            "curso": codigo,
            "nota": nota,
            "frequencia": frequencia,
        })

    def registrar_resultado_matricula(self, curso, nota, frequencia, id_turma):
        """Inclui ou atualiza no histórico o resultado de uma matrícula concluída."""
        codigo = self._normalizar_codigo(curso)
        if not isinstance(id_turma, str) or not id_turma.strip():
            raise ValueError("ID da turma inválido para o histórico acadêmico.")

        nota = self._validar_numero(nota, "Nota", 0, 10)
        frequencia = self._validar_numero(frequencia, "Frequência", 0, 100)
        id_turma = id_turma.strip().upper()

        for registro in self._historico:
            if registro.get("turma") == id_turma:
                registro.update({
                    "curso": codigo,
                    "nota": nota,
                    "frequencia": frequencia,
                })
                return

        self._historico.append({
            "curso": codigo,
            "nota": nota,
            "frequencia": frequencia,
            "turma": id_turma,
        })

    def remover_resultado_matricula(self, id_turma):
        """Remove do histórico o resultado ligado a uma matrícula trancada."""
        id_turma = str(id_turma).strip().upper()
        self._historico = [
            registro for registro in self._historico
            if registro.get("turma") != id_turma
        ]

    def aprovado_em(self, codigo_curso):
        codigo_curso = str(codigo_curso).strip().upper()
        return any(
            str(item.get("curso", "")).strip().upper() == codigo_curso
            and item.get("nota") is not None
            and item.get("frequencia") is not None
            and float(item["nota"]) >= settings.nota_minima_aprovacao
            and float(item["frequencia"]) >= settings.frequencia_minima
            for item in self._historico
        )
