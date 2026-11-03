"""Menus da aplicação CLI; delega cada operação ao módulo responsável."""

from cli.telas import (
    cadastrar_curso, editar_curso, remover_curso, listar_cursos,
    adicionar_prerequisito, remover_prerequisito,
    cadastrar_aluno, editar_aluno, remover_aluno, listar_alunos,
    criar_turma, remover_turma, abrir_turma, fechar_turma, listar_turmas,
    matricular_aluno, lancar_nota, lancar_frequencia, trancar_matricula,
    listar_matriculas,
)
from cli.relatorios import (
    relatorio_alunos_por_turma,
    relatorio_top_cr,
    relatorio_taxa_aprovacao,
    relatorio_distribuicao_notas,
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


def _executar_submenu(titulo, opcoes, acoes, dados):
    """Executa submenus com o mesmo fluxo de navegação."""
    while True:
        print(f"\n=== {titulo} ===")
        for numero, descricao in opcoes:
            print(f"{numero} - {descricao}")
        print("0 - Voltar")

        opcao = _ler_opcao()
        if opcao == "0":
            return

        acao = acoes.get(opcao)
        if acao is None:
            print("Opção inválida.")
            continue
        acao(dados)


def menu_cursos(dados):
    _executar_submenu(
        "CURSOS",
        [("1", "Cadastrar curso"), ("2", "Listar cursos"),
         ("3", "Editar curso"), ("4", "Remover curso"),
         ("5", "Adicionar pré-requisito"), ("6", "Remover pré-requisito")],
        {"1": cadastrar_curso, "2": listar_cursos, "3": editar_curso,
         "4": remover_curso, "5": adicionar_prerequisito,
         "6": remover_prerequisito},
        dados,
    )


def menu_alunos(dados):
    _executar_submenu(
        "ALUNOS",
        [("1", "Cadastrar aluno"), ("2", "Listar alunos"),
         ("3", "Editar aluno"), ("4", "Remover aluno")],
        {"1": cadastrar_aluno, "2": listar_alunos,
         "3": editar_aluno, "4": remover_aluno},
        dados,
    )


def menu_turmas(dados):
    _executar_submenu(
        "TURMAS",
        [("1", "Criar turma"), ("2", "Listar turmas"),
         ("3", "Abrir turma"), ("4", "Fechar turma"),
         ("5", "Remover turma")],
        {"1": criar_turma, "2": listar_turmas, "3": abrir_turma,
         "4": fechar_turma, "5": remover_turma},
        dados,
    )


def menu_matriculas(dados):
    _executar_submenu(
        "MATRÍCULAS",
        [("1", "Matricular aluno"), ("2", "Lançar nota"),
         ("3", "Lançar frequência"), ("4", "Trancar matrícula"),
         ("5", "Listar matrículas")],
        {"1": matricular_aluno, "2": lancar_nota,
         "3": lancar_frequencia, "4": trancar_matricula,
         "5": listar_matriculas},
        dados,
    )


def menu_relatorios(dados):
    _executar_submenu(
        "RELATÓRIOS",
        [("1", "Alunos por turma e ocupação"),
         ("2", "Top N alunos por CR no período"),
         ("3", "Taxa de aprovação por curso e turma"),
         ("4", "Distribuição de notas"),
         ("5", "Alunos em risco")],
        {"1": relatorio_alunos_por_turma, "2": relatorio_top_cr,
         "3": relatorio_taxa_aprovacao,
         "4": relatorio_distribuicao_notas,
         "5": relatorio_alunos_em_risco},
        dados,
    )
