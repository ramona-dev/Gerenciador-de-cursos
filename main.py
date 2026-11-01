from persistencia.carregador import carregar_sistema
from cli.menu import executar_menu


def main():

    dados = carregar_sistema()

    executar_menu(dados)


if __name__ == "__main__":
    main()