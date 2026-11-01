from persistencia.carregador import carregar_sistema
from cli.menu import iniciar_menu


def main():

    dados = carregar_sistema()

    iniciar_menu(dados)


if __name__ == "__main__":
    main()