# dados.py

import json
from pathlib import Path


BASE_DIR = Path(__file__).parent

ARQUIVO = BASE_DIR / "dados.json"
SETTINGS = BASE_DIR.parent / "settings.json"


def estrutura_vazia():
    """
    Estrutura padrão utilizada quando não existem dados.
    """
    return {
        "alunos": [],
        "cursos": [],
        "turmas": [],
        "matriculas": []
    }


def salvar_tudo(alunos, cursos, turmas, matriculas):
    """
    Salva todos os dados do sistema em JSON.
    """

    dados = {
        "alunos": [
            {
                "matricula": aluno.matricula,
                "nome": aluno.nome,
                "email": aluno.email,
                "historico": aluno.historico
            }
            for aluno in alunos
        ],

        "cursos": [
            {
                "codigo": curso.codigo,
                "nome": curso.nome,
                "carga_horaria": curso.carga_horaria,
                "prerequisitos": curso.prerequisitos
            }
            for curso in cursos
        ],

        "turmas": [
            {
                "id": turma.id,
                "curso_codigo": turma.curso.codigo,
                "semestre": turma.semestre,
                "dias_horarios": turma.horarios,
                "vagas": turma.vagas,

                # Até existir @property local
                "local": getattr(turma, "_local", ""),

                "aberta": turma.aberta
            }
            for turma in turmas
        ],

        "matriculas": [
            {
                "aluno": matricula.aluno.matricula,
                "turma": matricula.turma.id,
                "nota": matricula.nota,
                "frequencia": matricula.frequencia,
                "ativa": matricula.ativa,
                "data": str(matricula.data)
            }
            for matricula in matriculas
        ]
    }

    ARQUIVO.write_text(
        json.dumps(
            dados,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


def carregar_tudo():
    """
    Carrega todos os dados persistidos.
    """

    if not ARQUIVO.exists():
        return estrutura_vazia()

    try:
        conteudo = ARQUIVO.read_text(
            encoding="utf-8"
        ).strip()

        if not conteudo:
            return estrutura_vazia()

        return json.loads(conteudo)

    except json.JSONDecodeError:
        print("Erro ao carregar JSON. Estrutura reiniciada.")
        return estrutura_vazia()


def carregar_settings():
    """
    Carrega configurações do sistema.
    Caso não exista arquivo, cria um padrão.
    """

    configuracao_padrao = {
        "nota_minima_aprovacao": 6.0,
        "frequencia_minima": 75.0,
        "data_limite_trancamento": "2025-06-30",
        "max_turmas_por_aluno": None,
        "top_n_alunos": 5
    }

    if not SETTINGS.exists():

        SETTINGS.write_text(
            json.dumps(
                configuracao_padrao,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        return configuracao_padrao

    try:
        return json.loads(
            SETTINGS.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError:
        print("Erro em settings.json. Utilizando configurações padrão.")
        return configuracao_padrao
