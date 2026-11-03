"""Menus da aplicação CLI."""

from cli.telas import (
    cadastrar_curso, editar_curso, remover_curso, listar_cursos,
    adicionar_prerequisito, remover_prerequisito,
    cadastrar_aluno, editar_aluno, remover_aluno, listar_alunos,
    criar_turma, remover_turma, abrir_turma, fechar_turma, listar_turmas,
    matricular_aluno, lancar_nota, lancar_frequencia, trancar_matricula,
    listar_matriculas, relatorio_alunos_por_turma, relatorio_top_cr,
    relatorio_taxa_aprovacao, relatorio_distribuicao_notas,
    relatorio_alunos_em_risco,
)


def _ler_opcao(mensagem="Escolha uma opção: "):
    return input(mensagem).strip()


def executar_menu(dados):
    while True:
        print("\n" + "=" * 42)
        print(" GERENCIADOR DE CURSOS ")
        print("=" * 42)
        print("1 - Cursos")
        print("2 - Alunos")
        print("3 - Turmas")
        print("4 - Matrículas")
        print("5 - Relatórios")
        print("0 - Sair")
        opcao = _ler_opcao("\nEscolha uma opção: ")

        if opcao == "1":
            menu_cursos(dados)
        elif opcao == "2":
            menu_alunos(dados)
        elif opcao == "3":
            menu_turmas(dados)
        elif opcao == "4":
            menu_matriculas(dados)
        elif opcao == "5":
            menu_relatorios(dados)
        elif opcao == "0":
            print("\nEncerrando sistema...")
            break
        else:
            print("\nOpção inválida.")


def menu_cursos(dados):
    while True:
        print("\n=== CURSOS ===")
        print("1 - Cadastrar curso")
        print("2 - Listar cursos")
        print("3 - Editar curso")
        print("4 - Remover curso")
        print("5 - Adicionar pré-requisito")
        print("6 - Remover pré-requisito")
        print("0 - Voltar")
        opcao = _ler_opcao()
        acoes = {
            "1": cadastrar_curso,
            "2": listar_cursos,
            "3": editar_curso,
            "4": remover_curso,
            "5": adicionar_prerequisito,
            "6": remover_prerequisito,
        }
        if opcao == "0":
            return
        acao = acoes.get(opcao)
        if acao:
            acao(dados)
        else:
            print("Opção inválida.")


def menu_alunos(dados):
    while True:
        print("\n=== ALUNOS ===")
        print("1 - Cadastrar aluno")
        print("2 - Listar alunos")
        print("3 - Editar aluno")
        print("4 - Remover aluno")
        print("0 - Voltar")
        opcao = _ler_opcao()
        acoes = {"1": cadastrar_aluno, "2": listar_alunos, "3": editar_aluno, "4": remover_aluno}
        if opcao == "0":
            return
        acao = acoes.get(opcao)
        if acao:
            acao(dados)
        else:
            print("Opção inválida.")


def menu_turmas(dados):
    while True:
        print("\n=== TURMAS ===")
        print("1 - Criar turma")
        print("2 - Listar turmas")
        print("3 - Abrir turma")
        print("4 - Fechar turma")
        print("5 - Remover turma")
        print("0 - Voltar")
        opcao = _ler_opcao()
        acoes = {"1": criar_turma, "2": listar_turmas, "3": abrir_turma,
                 "4": fechar_turma, "5": remover_turma}
        if opcao == "0":
            return
        acao = acoes.get(opcao)
        if acao:
            acao(dados)
        else:
            print("Opção inválida.")


def menu_matriculas(dados):
    while True:
        print("\n=== MATRÍCULAS ===")
        print("1 - Matricular aluno")
        print("2 - Lançar nota")
        print("3 - Lançar frequência")
        print("4 - Trancar matrícula")
        print("5 - Listar matrículas")
        print("0 - Voltar")
        opcao = _ler_opcao()
        acoes = {"1": matricular_aluno, "2": lancar_nota,
                 "3": lancar_frequencia, "4": trancar_matricula,
                 "5": listar_matriculas}
        if opcao == "0":
            return
        acao = acoes.get(opcao)
        if acao:
            acao(dados)
        else:
            print("Opção inválida.")


def menu_relatorios(dados):
    while True:
        print("\n=== RELATÓRIOS ===")
        print("1 - Alunos por turma")
        print("2 - Top N alunos por CR")
        print("3 - Taxa de aprovação")
        print("4 - Distribuição de notas")
        print("5 - Alunos em risco")
        print("0 - Voltar")
        opcao = _ler_opcao()
        acoes = {"1": relatorio_alunos_por_turma, "2": relatorio_top_cr,
                 "3": relatorio_taxa_aprovacao, "4": relatorio_distribuicao_notas,
                 "5": relatorio_alunos_em_risco}
        if opcao == "0":
            return
        acao = acoes.get(opcao)
        if acao:
            acao(dados)
        else:
            print("Opção inválida.")
