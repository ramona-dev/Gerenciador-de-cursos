from cli.telas import (
    listar_cursos,
    listar_alunos,
    listar_turmas,
    listar_matriculas,
    relatorio_alunos_por_turma,
    relatorio_top_cr
)


def executar_menu(dados):

    while True:

        print("\n=== GERENCIADOR DE CURSOS ===")
        print("1 - Cursos")
        print("2 - Alunos")
        print("3 - Turmas")
        print("4 - Matrículas")
        print("5 - Relatórios")
        print("0 - Sair")

        opcao = input("\nEscolha: ")

        if opcao == "1":
            listar_cursos(dados)

        elif opcao == "2":
            listar_alunos(dados)

        elif opcao == "3":
            listar_turmas(dados)

        elif opcao == "4":
            listar_matriculas(dados)

        elif opcao == "5":
            menu_relatorios(dados)

        elif opcao == "0":
            print("Encerrando...")
            break

        else:
            print("Opção inválida.")


def menu_relatorios(dados):

    while True:

        print("\n=== RELATÓRIOS ===")
        print("1 - Alunos por turma")
        print("2 - Top CR")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            relatorio_alunos_por_turma(dados)

        elif opcao == "2":
            relatorio_top_cr(dados)

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")