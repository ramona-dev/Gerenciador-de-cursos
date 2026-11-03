import pytest
from types import SimpleNamespace

from modulos.curso import Curso
from modulos.aluno import Aluno
from modulos.turma import Turma, parse_horario, normalizar_dias
import settings


def setup_turma_basica():
    curso = Curso("POO101", "POO", 60)
    turma = Turma(curso, "T1", "2025.2", {"seg": "08:00-10:00"}, vagas=2)
    return curso, turma


def test_criacao_turma_valida():
    curso, turma = setup_turma_basica()
    assert turma.curso == curso
    assert turma.id == "T1"
    assert "seg" in turma.horarios
    assert turma.vagas == 2


def test_len_retorna_qtd_matriculas_ativas(aluno_fixture):
    _, turma = setup_turma_basica()
    turma._matriculas[aluno_fixture] = None
    assert len(turma) == 0


def test_tem_choque_de_horario():
    curso = Curso("POO101", "POO", 60)
    turma1 = Turma(curso, "T1", "2025.2", {"seg": "08:00-10:00"}, vagas=30)
    turma2 = Turma(curso, "T2", "2025.2", {"seg": "09:00-11:00"}, vagas=30)
    assert turma1.tem_choque(turma2) is True


def test_nao_tem_choque_em_semestres_diferentes():
    curso = Curso("POO101", "POO", 60)
    turma1 = Turma(curso, "T1", "2025.1", {"seg": "08:00-10:00"}, vagas=30)
    turma2 = Turma(curso, "T2", "2025.2", {"seg": "09:00-11:00"}, vagas=30)
    assert turma1.tem_choque(turma2) is False


def test_matricula_negada_por_turma_fechada():
    _, turma = setup_turma_basica()
    aluno = Aluno("2025001", "Maria", "maria@email.com")
    turma.fechar()
    with pytest.raises(ValueError, match="Turma está fechada"):
        turma.adicionar_aluno(aluno, settings.obter_configuracoes())


def test_matricula_negada_por_turma_lotada():
    _, turma = setup_turma_basica()
    aluno1 = Aluno("2025001", "Maria", "maria@email.com")
    aluno2 = Aluno("2025002", "João", "joao@email.com")
    aluno3 = Aluno("2025003", "Ana", "ana@email.com")
    turma._matriculas[aluno1] = SimpleNamespace(ativa=True)
    turma._matriculas[aluno2] = SimpleNamespace(ativa=True)
    with pytest.raises(ValueError, match="lotada"):
        turma.adicionar_aluno(aluno3, settings.obter_configuracoes())


def test_matricula_negada_por_prerequisito():
    curso_avancado = Curso("POO101", "POO", 60, prerequisitos=["MAT101"])
    turma = Turma(curso_avancado, "T1", "2025.2", {"seg": "08:00-10:00"}, vagas=30)
    aluno = Aluno("2025001", "Maria", "maria@email.com")
    with pytest.raises(ValueError, match="pré-requisito"):
        turma.adicionar_aluno(aluno, settings.obter_configuracoes())


def test_matricula_negada_por_choque_de_horario():
    curso = Curso("POO101", "POO", 60)
    turma1 = Turma(curso, "T1", "2025.2", {"seg": "08:00-10:00"}, vagas=30)
    turma2 = Turma(curso, "T2", "2025.2", {"seg": "09:00-11:00"}, vagas=30)
    aluno = Aluno("2025001", "Maria", "maria@email.com")
    turma1._matriculas[aluno] = SimpleNamespace(ativa=True)
    aluno.adicionar_turma(turma1)
    with pytest.raises(ValueError, match="Choque de horário"):
        turma2.adicionar_aluno(aluno, settings.obter_configuracoes())


def test_normaliza_dias_digitados_juntos():
    assert normalizar_dias("seg qua") == ["seg", "qua"]
    assert normalizar_dias("seg,qua") == ["seg", "qua"]


def test_rejeita_dia_invalido():
    with pytest.raises(ValueError, match="inválido"):
        normalizar_dias("segunda-feira")


def test_rejeita_horario_invalido():
    with pytest.raises(ValueError):
        parse_horario("25:00-26:00")


def test_rejeita_horario_com_fim_antes_do_inicio():
    with pytest.raises(ValueError, match="posterior"):
        parse_horario("10:00-08:00")


def test_rejeita_id_turma_vazio():
    curso = Curso("POO101", "POO", 60)
    with pytest.raises(ValueError, match="ID"):
        Turma(curso, "  ", "2025.2", {"seg": "08:00-10:00"}, 10)
