import json
from pathlib import Path
class JsonManager:

    @staticmethod
    def salvar(caminho, dados):
        with open(
            caminho,
            "w",
            encoding="utf-8"
        ) as arquivo:

            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4
            )
    @staticmethod
    def carregar(caminho):

        arquivo = Path(caminho)

        if not arquivo.exists():
            return []

        with open(
            caminho,
            encoding="utf-8"
        ) as f:

            return json.load(f)