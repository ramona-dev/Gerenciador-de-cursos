import pytest
from modulos.pessoa import Pessoa
from modulos.aluno import Aluno

class CursoFake:
    def __init__(self, codigo):
        self.codigo = codigo

def test_criacao_aluno_valido():
    aluno = Aluno("2025001", "Maria", "maria@email.com")
    assert aluno.matricula == "2025001"
    assert aluno.nome == "Maria"
    assert aluno.email == "maria@email.com"
    assert aluno.historico == []
    assert aluno.turmas == []

def test_matricula_vazia_gera_erro():
    with pytest.raises(ValueError):
        Aluno("", "João", "joao@email.com")

def test_adicionar_disciplina_e_calculo_cr():
    aluno = Aluno("2025002", "Ana", "ana@email.com")
    curso = CursoFake("POO101")
    aluno.adicionar_disciplina(curso, nota=8.0, frequencia=90)
    aluno.adicionar_disciplina(curso, nota=6.0, frequencia=80)
    assert len(aluno.historico) == 2
    assert pytest.approx(aluno.calculo_de_CR(), 0.01) == 7.0

def test_aprovado_em_disciplina():
    aluno = Aluno("2025003", "Carlos", "carlos@email.com")
    curso = CursoFake("POO101")
    aluno.adicionar_disciplina(curso, nota=7.0, frequencia=80)
    assert aluno.aprovado_em("POO101") is True
    assert aluno.aprovado_em("POO999") is False

def test_ordem_por_cr_e_nome():
    aluno1 = Aluno("2025004", "Beatriz", "bia@email.com")
    aluno2 = Aluno("2025005", "André", "andre@email.com")
    curso = CursoFake("POO101")
    aluno1.adicionar_disciplina(curso, nota=8.0, frequencia=90)
    aluno2.adicionar_disciplina(curso, nota=8.0, frequencia=90)
    # CR igual → ordena por nome
    assert sorted([aluno1, aluno2])[0].nome == "André"
