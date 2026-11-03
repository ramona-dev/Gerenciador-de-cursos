"""Testes adicionais para validar o formato numérico da matrícula."""

import pytest

from modulos.aluno import Aluno


@pytest.mark.parametrize(
    "matricula",
    ["ABC", "12A3", "12-34", "12.34", "１２３"],
)
def test_aluno_rejeita_matricula_que_nao_contem_apenas_digitos(matricula):
    with pytest.raises(ValueError, match="somente números"):
        Aluno(matricula, "Maria Silva", "maria@email.com")


def test_aluno_preserva_zeros_a_esquerda_na_matricula():
    aluno = Aluno("002345", "Maria Silva", "maria@email.com")
    assert aluno.matricula == "002345"


def test_from_dict_rejeita_matricula_com_letras():
    dados = {
        "matricula": "20A5001",
        "nome": "Maria Silva",
        "email": "maria@email.com",
        "historico": [],
    }

    with pytest.raises(ValueError, match="somente números"):
        Aluno.from_dict(dados)


def test_cadastro_cli_rejeita_matricula_com_letras_e_pede_nova(
    monkeypatch, capsys, tmp_path
):
    from cli import telas
    import persistencia.json_manager as json_manager

    dados = {"alunos": []}
    entradas = iter([
        "ABC",
        "2026002",
        "Ana Souza",
        "ana@email.com",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _mensagem="": next(entradas),
    )
    monkeypatch.setattr(telas, "pausar", lambda: None)
    monkeypatch.setattr(json_manager, "BASE_DIR", tmp_path)

    telas.cadastrar_aluno(dados)

    assert len(dados["alunos"]) == 1
    assert dados["alunos"][0].matricula == "2026002"
    assert "somente números" in capsys.readouterr().out
