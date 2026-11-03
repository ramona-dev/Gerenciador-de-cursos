"""Carrega e valida as configurações do sistema a partir de settings.json."""

import json
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CAMINHO_CONFIG = BASE_DIR / "settings.json"

PADROES = {
    "nota_minima_aprovacao": 6.0,
    "frequencia_minima": 75.0,
    "data_limite_trancamento": "2027-12-30",
    "max_turmas_por_aluno": None,
    "top_n_alunos": 5,
}


def carregar_configuracoes(caminho=None):
    """Retorna configurações validadas, completando campos ausentes com padrões."""
    arquivo = Path(caminho) if caminho else CAMINHO_CONFIG
    if not arquivo.is_absolute():
        arquivo = BASE_DIR / arquivo

    configuracoes = dict(PADROES)
    if arquivo.exists():
        try:
            with arquivo.open(encoding="utf-8") as entrada:
                dados = json.load(entrada)
        except json.JSONDecodeError as erro:
            raise ValueError(
                f"Arquivo de configurações inválido ({arquivo}): {erro}"
            ) from erro
        if not isinstance(dados, dict):
            raise ValueError("settings.json deve conter um objeto JSON.")
        configuracoes.update(dados)

    try:
        nota = float(configuracoes["nota_minima_aprovacao"])
        frequencia = float(configuracoes["frequencia_minima"])
        top_n = int(configuracoes["top_n_alunos"])
        date.fromisoformat(str(configuracoes["data_limite_trancamento"]))
    except (TypeError, ValueError, KeyError) as erro:
        raise ValueError("Há uma configuração inválida em settings.json.") from erro

    if not 0 <= nota <= 10:
        raise ValueError("nota_minima_aprovacao deve estar entre 0 e 10.")
    if not 0 <= frequencia <= 100:
        raise ValueError("frequencia_minima deve estar entre 0 e 100.")
    if top_n <= 0:
        raise ValueError("top_n_alunos deve ser maior que zero.")

    limite = configuracoes.get("max_turmas_por_aluno")
    if limite is not None:
        try:
            limite = int(limite)
        except (TypeError, ValueError) as erro:
            raise ValueError("max_turmas_por_aluno deve ser inteiro ou null.") from erro
        if limite <= 0:
            raise ValueError("max_turmas_por_aluno deve ser maior que zero ou null.")

    configuracoes["nota_minima_aprovacao"] = nota
    configuracoes["frequencia_minima"] = frequencia
    configuracoes["top_n_alunos"] = top_n
    configuracoes["max_turmas_por_aluno"] = limite
    configuracoes["data_limite_trancamento"] = str(
        configuracoes["data_limite_trancamento"]
    )
    return configuracoes


def salvar_configuracoes(configuracoes, caminho=None):
    arquivo = Path(caminho) if caminho else CAMINHO_CONFIG
    if not arquivo.is_absolute():
        arquivo = BASE_DIR / arquivo
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    with arquivo.open("w", encoding="utf-8") as saida:
        json.dump(configuracoes, saida, ensure_ascii=False, indent=4)


_CONFIG = carregar_configuracoes()
nota_minima_aprovacao = _CONFIG["nota_minima_aprovacao"]
frequencia_minima = _CONFIG["frequencia_minima"]
data_limite_trancamento = _CONFIG["data_limite_trancamento"]
max_turmas_por_aluno = _CONFIG["max_turmas_por_aluno"]
top_n_alunos = _CONFIG["top_n_alunos"]


def obter_configuracoes():
    """Devolve uma cópia das configurações usadas pelas regras de negócio."""
    return dict(_CONFIG)
