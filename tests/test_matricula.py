import pytest
from datetime import date, timedelta
from modulos.matricula import Matricula
from modulos.aluno import Aluno
from modulos.curso import Curso
from modulos.turma import Turma
import settings

def setup_aluno_e_turma():
    aluno = Aluno("2025001", "Maria", "maria@email.com")
    curso = Curso("POO101", "POO", 60)
    turma = Turma("T1", curso, "2025.2", {"seg":"10:00-12:00"}, vagas=30)
    return aluno, turma

def test_criacao_matricula_valida():
    aluno, turma = setup_aluno_e_turma()
    m = Matricula(aluno, turma)
    assert m.aluno == aluno
    assert m.turma == turma
    assert m.nota is None
    assert m.frequencia is None
    assert m.ativa is True
    assert m.data == date.today()

def test_lancar_nota_valida_e_invalida():
    aluno, turma = setup_aluno_e_turma()
    m = Matricula(aluno, turma)
    m.lancar_nota(8.5)
    assert m.nota == 8.5
    with pytest.raises(ValueError):
        m.lancar_nota(11)

def test_lancar_frequencia_valida_e_invalida():
    aluno, turma = setup_aluno_e_turma()
    m = Matricula(aluno, turma)
    m.lancar_frequencia(90)
    assert m.frequencia == 90
    with pytest.raises(ValueError):
        m.lancar_frequencia(120)

def test_trancar_respeitando_data_limite(monkeypatch):
    aluno, turma = setup_aluno_e_turma()
    m = Matricula(aluno, turma)
    # simula data dentro do prazo
    monkeypatch.setattr("matricula.date.today", lambda: date.fromisoformat(settings.data_limite_trancamento))
    m.trancar(settings.__dict__)
    assert m.ativa is False

def test_situacao_aprovado_reprovado_cursando_trancado():
    aluno, turma = setup_aluno_e_turma()
    m = Matricula(aluno, turma)
    # sem nota/frequência
    assert m.situacao() == "CURSANDO"
    # aprovado
    m.lancar_nota(settings.nota_minima_aprovacao)
    m.lancar_frequencia(settings.frequencia_minima)
    assert m.situacao() == "APROVADO"
    # reprovado
    m.lancar_nota(5.0)
    m.lancar_frequencia(60)
    assert m.situacao() == "REPROVADO"
    # trancado
    m._ativa = False
    assert m.situacao() == "TRANCADA"
