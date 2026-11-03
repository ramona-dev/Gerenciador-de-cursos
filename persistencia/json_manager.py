"""Leitura e gravação segura dos arquivos JSON do projeto."""

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


class JsonManager:
    @staticmethod
    def resolver_caminho(caminho):
        arquivo = Path(caminho)
        return arquivo if arquivo.is_absolute() else BASE_DIR / arquivo

    @staticmethod
    def salvar(caminho, dados):
        arquivo = JsonManager.resolver_caminho(caminho)
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        temporario = arquivo.with_suffix(arquivo.suffix + ".tmp")
        try:
            with temporario.open("w", encoding="utf-8") as saida:
                json.dump(dados, saida, ensure_ascii=False, indent=4)
                saida.write("\n")
            os.replace(temporario, arquivo)
        finally:
            if temporario.exists():
                temporario.unlink()

    @staticmethod
    def carregar(caminho):
        arquivo = JsonManager.resolver_caminho(caminho)
        if not arquivo.exists():
            return []
        try:
            with arquivo.open(encoding="utf-8") as entrada:
                dados = json.load(entrada)
        except json.JSONDecodeError as erro:
            raise ValueError(f"JSON inválido em {arquivo}: {erro}") from erro
        return dados
