import pytest

from modulos.aluno import Aluno
from modulos.curso import Curso
from modulos.historico_academico import HistoricoAcademico
from modulos.pessoa import Pessoa


def test_criacao_aluno_valido():
    aluno = Aluno("2025001", "Maria", "maria@email.com")
    assert aluno.matricula == "2025001"
    assert aluno.nome == "Maria"
    assert aluno.email == "maria@email.com"
    assert aluno.historico == []
    assert aluno.turmas == []


def test_aluno_usa_heranca_multipla():
    aluno = Aluno("2025001", "Maria", "maria@email.com")
    assert isinstance(aluno, Pessoa)
    assert isinstance(aluno, HistoricoAcademico)


def test_aluno_possui_heranca_multipla():
    mro = Aluno.__mro__
    assert Pessoa in mro
    assert HistoricoAcademico in mro


def test_matricula_vazia_gera_erro():
    with pytest.raises(ValueError):
        Aluno("", "João", "joao@email.com")


def test_adicionar_disciplina_e_calculo_cr():
    aluno = Aluno("2025002", "Ana", "ana@email.com")
    curso = Curso("POO101", "POO", 60)
    aluno.adicionar_disciplina(curso, nota=8.0, frequencia=90)
    aluno.adicionar_disciplina(curso, nota=6.0, frequencia=80)
    assert len(aluno.historico) == 2
    assert aluno.calculo_de_CR() == pytest.approx(7.0)


def test_cr_sem_historico_e_zero():
    aluno = Aluno("2025003", "Carlos", "carlos@email.com")
    assert aluno.cr == 0.0


def test_aprovado_em_disciplina():
    aluno = Aluno("2025004", "Carlos", "carlos@email.com")
    curso = Curso("POO101", "POO", 60)
    aluno.adicionar_disciplina(curso, nota=7.0, frequencia=80)
    assert aluno.aprovado_em("POO101") is True
    assert aluno.aprovado_em("POO999") is False


def test_reprovado_nao_cumpre_prerequisito():
    aluno = Aluno("2025005", "Joana", "joana@email.com")
    curso = Curso("MAT101", "Matemática", 60)
    aluno.adicionar_disciplina(curso, nota=5.0, frequencia=90)
    assert aluno.aprovado_em("MAT101") is False


def test_ordem_por_cr_e_nome():
    aluno1 = Aluno("2025006", "Beatriz", "bia@email.com")
    aluno2 = Aluno("2025007", "André", "andre@email.com")
    curso = Curso("POO101", "POO", 60)
    aluno1.adicionar_disciplina(curso, nota=8.0, frequencia=90)
    aluno2.adicionar_disciplina(curso, nota=8.0, frequencia=90)
    assert sorted([aluno1, aluno2])[0].nome == "André"


def test_email_invalido_na_criacao():
    with pytest.raises(ValueError):
        Aluno("2025008", "Pedro", "email-invalido")


def test_from_dict_rejeita_nota_invalida_no_historico():
    dados = {
        "matricula": "2025010",
        "nome": "João",
        "email": "joao@email.com",
        "historico": [{"curso": "MAT101", "nota": 11, "frequencia": 80}],
    }
    with pytest.raises(ValueError, match="Nota do histórico"):
        Aluno.from_dict(dados)


def test_from_dict_rejeita_curso_inexistente_no_historico():
    dados = {
        "matricula": "2025011",
        "nome": "João",
        "email": "joao@email.com",
        "historico": [{"curso": "MAT999", "nota": 8, "frequencia": 80}],
    }
    with pytest.raises(ValueError, match="curso inexistente"):
        Aluno.from_dict(dados, codigos_cursos={"MAT101": object()})
