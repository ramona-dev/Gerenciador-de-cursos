import pytest
from modulos.curso import Curso
from modulos.aluno import Aluno
from modulos.turma import Turma

def setup_turma_basica():
    curso = Curso("POO101", "POO", 60)
    turma = Turma(curso, "T1", "2025.2", {"seg":"08:00-10:00"}, vagas=2)
    return curso, turma

def test_criacao_turma_valida():
    curso, turma = setup_turma_basica()
    assert turma.curso == curso
    assert turma.id == "T1"
    assert "seg" in turma.horarios
    assert turma.vagas == 2

def test_len_retorna_qtd_matriculas_ativas(aluno_fixture):
    curso, turma = setup_turma_basica()
    aluno = aluno_fixture
    turma._matriculas[aluno] = None
    assert len(turma) == 0  # ainda não tem matrícula ativa

def test_tem_choque_de_horario():
    curso = Curso("POO101", "POO", 60)
    turma1 = Turma(curso, "T1", "2025.2", {"seg":"08:00-10:00"}, vagas=30)
    turma2 = Turma(curso, "T2", "2025.2", {"seg":"09:00-11:00"}, vagas=30)
    assert turma1.tem_choque(turma2) is True

def test_matricula_negada_por_turma_fechada(settings):
    curso, turma = setup_turma_basica()
    aluno = Aluno("2025001", "Maria", "maria@email.com")
    turma.fechar()
    with pytest.raises(ValueError, match="Turma está fechada."):
        turma.adicionar_aluno(aluno, settings.__dict__)

def test_matricula_negada_por_turma_lotada(settings):
    curso, turma = setup_turma_basica()
    aluno1 = Aluno("2025001", "Maria", "maria@email.com")
    aluno2 = Aluno("2025002", "João", "joao@email.com")
    aluno3 = Aluno("2025003", "Ana", "ana@email.com")
    turma.adicionar_aluno(aluno1, settings.__dict__)
    turma.adicionar_aluno(aluno2, settings.__dict__)
    with pytest.raises(ValueError, match="Turma está lotada."):
        turma.adicionar_aluno(aluno3, settings.__dict__)

def test_matricula_negada_por_prerequisito(settings):
    curso_base = Curso("MAT101", "Matemática", 40)
    curso_avancado = Curso("POO101", "POO", 60, prerequisitos=["MAT101"])
    turma = Turma(curso_avancado, "T1", "2025.2", {"seg":"08:00-10:00"}, vagas=30)
    aluno = Aluno("2025001", "Maria", "maria@email.com")
    with pytest.raises(ValueError, match="pré-requisito MAT101"):
        turma.adicionar_aluno(aluno, settings.__dict__)

def test_matricula_negada_por_choque_de_horario(settings):
    curso = Curso("POO101", "POO", 60)
    turma1 = Turma(curso, "T1", "2025.2", {"seg":"08:00-10:00"}, vagas=30)
    turma2 = Turma(curso, "T2", "2025.2", {"seg":"09:00-11:00"}, vagas=30)
    aluno = Aluno("2025001", "Maria", "maria@email.com")
    turma1.adicionar_aluno(aluno, settings.__dict__)
    aluno._turmas.append(turma1)  # simula vínculo
    with pytest.raises(ValueError, match="Choque de horário"):
        turma2.adicionar_aluno(aluno, settings.__dict__)
