import statistics
import settings
from modulos.curso import Curso
from modulos.aluno import Aluno
from persistencia.json_manager import JsonManager


def salvar_cursos(dados):

    JsonManager.salvar(
        "dados/cursos.json",
        [
            curso.to_dict()
            for curso in dados["cursos"]
        ]
    )
def salvar_alunos(dados):

    JsonManager.salvar(
        "dados/alunos.json",
        [
            aluno.to_dict()
            for aluno in dados["alunos"]
        ]
    )
def cadastrar_curso(dados):

    codigo = input(
        "Código: "
    )

    nome = input(
        "Nome: "
    )

    carga_horaria = int(
        input(
            "Carga horária: "
        )
    )

    curso = Curso(
        codigo,
        nome,
        carga_horaria
    )

    dados["cursos"].append(
        curso
    )

    salvar_cursos(dados)

    print(
        "\nCurso cadastrado."
    )

    input(
        "\nEnter para continuar..."
    )

def remover_curso(dados):

    codigo = input(
        "Código do curso: "
    )

    for curso in dados["cursos"]:

        if curso.codigo == codigo:

            dados["cursos"].remove(
                curso
            )

            salvar_cursos(dados)

            print(
                "\nCurso removido."
            )

            input(
                "\nEnter para continuar..."
            )

            return

    print(
        "\nCurso não encontrado."
    )

    input(
        "\nEnter para continuar..."
    )
def listar_cursos(dados):

    print("\n=== CURSOS ===")

    for curso in dados["cursos"]:
        print(curso)

    input("\nPressione Enter para continuar...")

def cadastrar_aluno(dados):

    matricula = input(
        "Matrícula: "
    )

    nome = input(
        "Nome: "
    )

    email = input(
        "Email: "
    )

    for aluno in dados["alunos"]:

        if (
            aluno.matricula
            == matricula
        ):

            print(
                "\nMatrícula já cadastrada."
            )

            input(
                "\nEnter para continuar..."
            )

            return

    aluno = Aluno(
        matricula,
        nome,
        email
    )

    dados["alunos"].append(
        aluno
    )

    salvar_alunos(dados)

    print(
        "\nAluno cadastrado."
    )

    input(
        "\nEnter para continuar..."
    )
def remover_aluno(dados):

    matricula = input(
        "Matrícula do aluno: "
    )

    for aluno in dados["alunos"]:

        if (
            aluno.matricula
            == matricula
        ):

            dados["alunos"].remove(
                aluno
            )

            salvar_alunos(dados)

            print(
                "\nAluno removido."
            )

            input(
                "\nEnter para continuar..."
            )

            return

    print(
        "\nAluno não encontrado."
    )

    input(
        "\nEnter para continuar..."
    )
def listar_alunos(dados):

    print("\n=== ALUNOS ===")

    for aluno in dados["alunos"]:

        print(
            f"{aluno.matricula}"
            f" - {aluno.nome}"
            f" | CR: {aluno.cr:.2f}"
        )

    input("\nPressione Enter para continuar...")


def listar_turmas(dados):

    print("\n=== TURMAS ===")

    for turma in dados["turmas"]:

        print(
            f"{turma.id}"
            f" - {turma.curso.nome}"
            f" ({len(turma)}/{turma.vagas})"
        )

    input("\nPressione Enter para continuar...")


def listar_matriculas(dados):

    print("\n=== MATRÍCULAS ===")

    for matricula in dados["matriculas"]:

        print(
            f"{matricula.aluno.nome}"
            f" -> {matricula.turma.id}"
            f" -> {matricula.situacao()}"
        )

    input("\nPressione Enter para continuar...")


def relatorio_alunos_por_turma(dados):

    print("\n=== ALUNOS POR TURMA ===")

    for turma in dados["turmas"]:

        print(
            f"\n{turma.id}"
            f" - {turma.curso.nome}"
        )

        if not turma.matriculas:

            print("Nenhum aluno matriculado.")
            continue

        for matricula in turma.matriculas:

            print(
                f" - {matricula.aluno.nome}"
            )

    input("\nPressione Enter para continuar...")


def relatorio_top_cr(dados):

    print("\n=== TOP CR ===")

    alunos = sorted(
        dados["alunos"],
        reverse=True
    )

    top_n = getattr(
        settings,
        "top_n_alunos",
        5
    )

    for posicao, aluno in enumerate(
        alunos[:top_n],
        start=1
    ):

        print(
            f"{posicao}º "
            f"{aluno.nome}"
            f" - CR {aluno.cr:.2f}"
        )

    input("\nPressione Enter para continuar...")


def relatorio_taxa_aprovacao(dados):

    print("\n=== TAXA DE APROVAÇÃO ===")

    for turma in dados["turmas"]:

        total = 0
        aprovados = 0

        for matricula in turma.matriculas:

            situacao = matricula.situacao()

            if situacao != "CURSANDO":
                total += 1

            if situacao == "APROVADO":
                aprovados += 1

        taxa = (
            (aprovados / total) * 100
            if total > 0
            else 0
        )

        print(
            f"{turma.id}"
            f" - {turma.curso.nome}"
            f" -> {taxa:.2f}%"
        )

    input("\nPressione Enter para continuar...")


def relatorio_distribuicao_notas(dados):

    print("\n=== DISTRIBUIÇÃO DE NOTAS ===")

    for turma in dados["turmas"]:

        notas = [
            matricula.nota
            for matricula in turma.matriculas
            if matricula.nota is not None
        ]

        print(
            f"\nTurma {turma.id}"
            f" - {turma.curso.nome}"
        )

        if not notas:

            print("Sem notas cadastradas.")
            continue

        media = statistics.mean(
            notas
        )

        mediana = statistics.median(
            notas
        )

        desvio = (
            statistics.stdev(notas)
            if len(notas) > 1
            else 0
        )

        print(
            f"Média: {media:.2f}"
        )

        print(
            f"Mediana: {mediana:.2f}"
        )

        print(
            f"Desvio padrão: {desvio:.2f}"
        )

    input("\nPressione Enter para continuar...")


def relatorio_alunos_em_risco(dados):

    print("\n=== ALUNOS EM RISCO ===")

    encontrou = False

    for matricula in dados["matriculas"]:

        nota = matricula.nota
        frequencia = matricula.frequencia

        risco_nota = (
            nota is not None
            and nota < settings.nota_minima_aprovacao
        )

        risco_frequencia = (
            frequencia is not None
            and frequencia < settings.frequencia_minima
        )

        if (
            risco_nota
            or risco_frequencia
        ):

            encontrou = True

            print(
                f"{matricula.aluno.nome}"
                f" | Turma: {matricula.turma.id}"
                f" | Nota: {nota}"
                f" | Frequência: {frequencia}"
            )

    if not encontrou:

        print(
            "Nenhum aluno em situação de risco."
        )

    input("\nPressione Enter para continuar...")