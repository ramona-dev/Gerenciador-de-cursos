"""Ponto de entrada do Gerenciador de Cursos."""

from persistencia.carregador import carregar_sistema
from cli.menu import executar_menu


def main():
    try:
        dados = carregar_sistema()
    except (ValueError, KeyError, TypeError, OSError) as erro:
        print(f"\nNão foi possível carregar os dados do sistema: {erro}")
        print("Corrija os arquivos JSON indicados antes de iniciar novamente.")
        return 1
    executar_menu(dados)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
