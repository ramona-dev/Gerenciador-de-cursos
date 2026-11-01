from cli.telas import (
    listar_cursos,
    listar_alunos,
    listar_turmas,
    cadastrar_curso,
    remover_curso,
    cadastrar_aluno,
    remover_aluno,
    listar_matriculas,
    relatorio_alunos_por_turma,
    relatorio_top_cr,
    relatorio_taxa_aprovacao,
    relatorio_distribuicao_notas,
    relatorio_alunos_em_risco
)
def menu_cursos(dados):

    while True:

        print("\n=== CURSOS ===")

        print("1 - Cadastrar curso")
        print("2 - Listar cursos")
        print("3 - Remover curso")
        print("0 - Voltar")

        opcao = input(
            "Escolha: "
        )

        if opcao == "1":

            cadastrar_curso(
                dados
            )

        elif opcao == "2":

            listar_cursos(
                dados
            )

        elif opcao == "3":

            remover_curso(
                dados
            )

        elif opcao == "0":

            break

        else:

            print(
                "Opção inválida."
            )
def executar_menu(dados):

    while True:

        print("\n" + "=" * 40)
        print(" GERENCIADOR DE CURSOS ")
        print("=" * 40)

        print("1 - Cursos")
        print("2 - Alunos")
        print("3 - Turmas")
        print("4 - Matrículas")
        print("5 - Relatórios")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            menu_cursos(dados)

        elif opcao == "2":
            menu_alunos(dados)

        elif opcao == "3":
            listar_turmas(dados)

        elif opcao == "4":
            listar_matriculas(dados)

        elif opcao == "5":
            menu_relatorios(dados)

        elif opcao == "0":
            print("\nEncerrando sistema...")
            break

        else:
            print("\nOpção inválida.")


def menu_relatorios(dados):

    while True:

        print("\n" + "=" * 40)
        print(" RELATÓRIOS ")
        print("=" * 40)

        print("1 - Alunos por turma")
        print("2 - Top N alunos por CR")
        print("3 - Taxa de aprovação")
        print("4 - Distribuição de notas")
        print("5 - Alunos em risco")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":

            relatorio_alunos_por_turma(
                dados
            )

        elif opcao == "2":

            relatorio_top_cr(
                dados
            )

        elif opcao == "3":

            relatorio_taxa_aprovacao(
                dados
            )

        elif opcao == "4":

            relatorio_distribuicao_notas(
                dados
            )

        elif opcao == "5":

            relatorio_alunos_em_risco(
                dados
            )

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida.")
def menu_alunos(dados):

    while True:

        print("\n=== ALUNOS ===")

        print(
            "1 - Cadastrar aluno"
        )

        print(
            "2 - Listar alunos"
        )

        print(
            "3 - Remover aluno"
        )

        print(
            "0 - Voltar"
        )

        opcao = input(
            "Escolha: "
        )

        if opcao == "1":

            cadastrar_aluno(
                dados
            )

        elif opcao == "2":

            listar_alunos(
                dados
            )

        elif opcao == "3":

            remover_aluno(
                dados
            )

        elif opcao == "0":

            break

        else:

            print(
                "Opção inválida."
            )