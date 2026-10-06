import pytest
from modulos.curso import Curso

def test_criacao_curso_valido():
    curso = Curso("POO101", "Programação Orientada a Objetos", 60)
    assert curso.codigo == "POO101"
    assert curso.nome == "Programação Orientada a Objetos"
    assert curso.carga_horaria == 60
    assert curso.prerequisitos == []

def test_codigo_invalido_gera_erro():
    with pytest.raises(ValueError):
        Curso("AB", "Curso Inválido", 40)

def test_nome_vazio_gera_erro():
    with pytest.raises(ValueError):
        Curso("MAT101", "   ", 40)

def test_carga_horaria_invalida_gera_erro():
    with pytest.raises(ValueError):
        Curso("HIS101", "História", 0)

def test_adicionar_prerequisito_valido():
    curso = Curso("POO101", "POO", 60)
    curso.adicionar_prerequisito("MAT101")
    assert "MAT101" in curso.prerequisitos

def test_prerequisito_repetido_gera_erro():
    curso = Curso("POO101", "POO", 60)
    curso.adicionar_prerequisito("MAT101")
    with pytest.raises(ValueError):
        curso.adicionar_prerequisito("MAT101")

def test_prerequisito_de_si_mesmo_gera_erro():
    curso = Curso("POO101", "POO", 60)
    with pytest.raises(ValueError):
        curso.adicionar_prerequisito("POO101")

def test_str_retorna_resumo_legivel():
    curso = Curso("POO101", "POO", 60)
    assert str(curso) == "POO101 - POO (60h)"
