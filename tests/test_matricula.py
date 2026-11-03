import pytest
from datetime import date

from modulos.matricula import Matricula
from modulos.aluno import Aluno
from modulos.curso import Curso
from modulos.turma import Turma
import settings


def setup_aluno_e_turma():
    aluno = Aluno("2025001", "Maria", "maria@email.com")
    curso = Curso("POO101", "POO", 60)
    turma = Turma(curso, "T1", "2025.2", {"seg": "10:00-12:00"}, vagas=30)
    return aluno, turma


def test_criacao_matricula_valida():
    aluno, turma = setup_aluno_e_turma()
    matricula = Matricula(aluno, turma)
    assert matricula.aluno == aluno
    assert matricula.turma == turma
    assert matricula.nota is None
    assert matricula.frequencia is None
    assert matricula.ativa is True
    assert matricula.data == date.today()
    assert turma in aluno.turmas
    assert len(turma) == 1


def test_lancar_nota_valida_e_invalida():
    aluno, turma = setup_aluno_e_turma()
    matricula = Matricula(aluno, turma)
    matricula.lancar_nota(8.5)
    assert matricula.nota == 8.5
    with pytest.raises(ValueError):
        matricula.lancar_nota(11)


def test_lancar_frequencia_valida_e_invalida():
    aluno, turma = setup_aluno_e_turma()
    matricula = Matricula(aluno, turma)
    matricula.lancar_frequencia(90)
    assert matricula.frequencia == 90
    with pytest.raises(ValueError):
        matricula.lancar_frequencia(120)


def test_trancar_respeitando_data_limite():
    aluno, turma = setup_aluno_e_turma()
    matricula = Matricula(aluno, turma)
    matricula.trancar(settings.obter_configuracoes())
    assert matricula.ativa is False
    assert turma not in aluno.turmas
    assert len(turma) == 0


def test_situacao_aprovado_reprovado_cursando_trancado():
    aluno, turma = setup_aluno_e_turma()
    matricula = Matricula(aluno, turma)
    assert matricula.situacao() == "CURSANDO"
    matricula.lancar_nota(settings.nota_minima_aprovacao)
    matricula.lancar_frequencia(settings.frequencia_minima)
    assert matricula.situacao() == "APROVADO"
    matricula.lancar_nota(5.0)
    matricula.lancar_frequencia(90)
    assert matricula.situacao() == "REPROVADO_POR_NOTA"
    matricula._ativa = False
    assert matricula.situacao() == "TRANCADA"


def test_matricula_trancada_nao_aceita_lancamento_de_nota():
    aluno, turma = setup_aluno_e_turma()
    matricula = Matricula(aluno, turma)
    matricula.trancar(settings.obter_configuracoes())
    with pytest.raises(ValueError, match="trancada"):
        matricula.lancar_nota(8.0)


def test_matricula_trancada_nao_aceita_lancamento_de_frequencia():
    aluno, turma = setup_aluno_e_turma()
    matricula = Matricula(aluno, turma)
    matricula.trancar(settings.obter_configuracoes())
    with pytest.raises(ValueError, match="trancada"):
        matricula.lancar_frequencia(80)


def test_from_dict_nao_reativa_turma_de_matricula_trancada():
    aluno, turma = setup_aluno_e_turma()
    dados = {
        "aluno": aluno.matricula,
        "turma": turma.id,
        "nota": None,
        "frequencia": 60,
        "ativa": False,
        "data": date.today().isoformat(),
    }
    matricula = Matricula.from_dict(dados, aluno, turma)
    assert matricula.situacao() == "TRANCADA"
    assert turma not in aluno.turmas
    assert len(turma) == 0
    assert matricula in turma.matriculas


def test_nao_permite_trancar_duas_vezes():
    aluno, turma = setup_aluno_e_turma()
    matricula = Matricula(aluno, turma)
    matricula.trancar(settings.obter_configuracoes())
    with pytest.raises(ValueError, match="já está trancada"):
        matricula.trancar(settings.obter_configuracoes())
