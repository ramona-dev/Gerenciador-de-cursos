import pytest

import settings
from cli import relatorios
from modulos.aluno import Aluno
from modulos.curso import Curso
from modulos.matricula import Matricula
from modulos.turma import Turma


@pytest.fixture(autouse=True)
def sem_pausa(monkeypatch):
    monkeypatch.setattr(relatorios, "pausar", lambda: None)


def montar_turma(curso, identificador, periodo="2026.2", vagas=3):
    return Turma(
        curso,
        identificador,
        periodo,
        {"seg": "08:00-10:00"},
        vagas,
    )


def test_relatorio_alunos_por_turma_informa_ocupacao_e_ignora_trancada(capsys):
    curso = Curso("POO101", "Programação", 60)
    turma = montar_turma(curso, "T1", vagas=2)
    ativa = Aluno("2026001", "Ana", "ana@email.com")
    trancada = Aluno("2026002", "Bia", "bia@email.com")

    matricula_ativa = Matricula(ativa, turma)
    matricula_trancada = Matricula(trancada, turma)
    matricula_trancada.trancar({"data_limite_trancamento": "2099-12-31"})

    dados = {
        "cursos": [curso], "alunos": [ativa, trancada],
        "turmas": [turma],
        "matriculas": [matricula_ativa, matricula_trancada],
    }
    relatorios.relatorio_alunos_por_turma(dados)
    saida = capsys.readouterr().out

    assert "Ocupação: 1/2 vagas" in saida
    assert "Ana" in saida
    assert "Bia" not in saida
    assert "Matrículas trancadas: 1" in saida


def test_taxa_aprovacao_ignora_matriculas_trancadas_e_incompletas(capsys):
    curso = Curso("POO101", "Programação", 60)
    turma1 = montar_turma(curso, "T1")
    turma2 = montar_turma(curso, "T2", periodo="2027.1")
    alunos = [
        Aluno("2026001", "Ana", "ana@email.com"),
        Aluno("2026002", "Bia", "bia@email.com"),
        Aluno("2026003", "Caio", "caio@email.com"),
    ]
    aprovada = Matricula(alunos[0], turma1)
    aprovada.lancar_nota(8)
    aprovada.lancar_frequencia(90)

    reprovada = Matricula(alunos[1], turma1)
    reprovada.lancar_nota(5)
    reprovada.lancar_frequencia(90)

    incompleta = Matricula(alunos[2], turma2)
    incompleta.lancar_nota(9)

    trancada_aluno = Aluno("2026004", "Duda", "duda@email.com")
    trancada = Matricula(trancada_aluno, turma2)
    trancada.lancar_nota(10)
    trancada.lancar_frequencia(90)
    trancada.trancar({"data_limite_trancamento": "2099-12-31"})

    alunos.append(trancada_aluno)
    dados = {
        "cursos": [curso], "alunos": alunos,
        "turmas": [turma1, turma2],
        "matriculas": [aprovada, reprovada, incompleta, trancada],
    }
    relatorios.relatorio_taxa_aprovacao(dados)
    saida = capsys.readouterr().out

    assert "TAXA DE APROVAÇÃO POR CURSO" in saida
    assert "POO101 - Programação: 50.00% (1/2)" in saida
    assert "T1 - Programação (2026.2): 50.00% (1/2)" in saida
    assert "T2 - Programação (2027.1): sem matrículas concluídas" in saida


def test_cr_no_periodo_considera_somente_turmas_do_periodo():
    curso = Curso("POO101", "Programação", 60)
    turma_2026 = montar_turma(curso, "T26", "2026.2")
    turma_2027 = montar_turma(curso, "T27", "2027.1")
    aluno = Aluno("2026001", "Ana", "ana@email.com")

    matricula_2026 = Matricula(aluno, turma_2026)
    matricula_2026.lancar_nota(8)
    matricula_2026.lancar_frequencia(90)

    matricula_2027 = Matricula(aluno, turma_2027)
    matricula_2027.lancar_nota(10)
    matricula_2027.lancar_frequencia(90)

    mapa_turmas = {turma_2026.id: turma_2026, turma_2027.id: turma_2027}
    assert relatorios.calcular_cr_no_periodo(aluno, "2026.2", mapa_turmas) == pytest.approx(8)
    assert relatorios.calcular_cr_no_periodo(aluno, "2027.1", mapa_turmas) == pytest.approx(10)
    assert relatorios.calcular_cr_no_periodo(aluno, "2025.2", mapa_turmas) is None


def test_top_cr_pede_periodo_e_filtra_ranking(monkeypatch, capsys):
    curso = Curso("POO101", "Programação", 60)
    turma_2026 = montar_turma(curso, "T26", "2026.2")
    turma_2027 = montar_turma(curso, "T27", "2027.1")
    ana = Aluno("2026001", "Ana", "ana@email.com")
    bia = Aluno("2026002", "Bia", "bia@email.com")

    for aluno, turma, nota in [
        (ana, turma_2026, 8),
        (ana, turma_2027, 10),
        (bia, turma_2026, 9),
    ]:
        matricula = Matricula(aluno, turma)
        matricula.lancar_nota(nota)
        matricula.lancar_frequencia(90)

    monkeypatch.setattr("builtins.input", lambda _="": "1")
    monkeypatch.setattr(settings, "top_n_alunos", 5)
    dados = {
        "cursos": [curso], "alunos": [ana, bia],
        "turmas": [turma_2026, turma_2027],
        "matriculas": [
            matricula for turma in [turma_2026, turma_2027]
            for matricula in turma.matriculas
        ],
    }
    relatorios.relatorio_top_cr(dados)
    saida = capsys.readouterr().out

    assert "Período: 2026.2" in saida
    assert "1º Bia - CR 9.00" in saida
    assert "2º Ana - CR 8.00" in saida


def test_taxa_aprovacao_sem_matriculas_concluidas_retorna_zero():
    aprovados, total, taxa = relatorios.calcular_resumo_aprovacao([])
    assert (aprovados, total, taxa) == (0, 0, 0.0)
