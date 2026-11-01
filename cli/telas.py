import statistics
import settings
from modulos.curso import Curso
from modulos.aluno import Aluno
from modulos.turma import Turma
from modulos.matricula import Matricula
from persistencia.json_manager import JsonManager

# Persistencia 
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
def salvar_turmas(dados):

    JsonManager.salvar(
        "dados/turmas.json",
        [
            turma.to_dict()
            for turma in dados["turmas"]
        ]
    )
def salvar_matriculas(dados):

    JsonManager.salvar(
        "dados/matriculas.json",
        [
            matricula.to_dict()
            for matricula in dados["matriculas"]
        ]
    )

    # CURSO 
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

# ALUNO 

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

# TURMAS 
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

# RELATÓRIOS
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
# TURMAS 
def criar_turma(dados):

    codigo_curso = input(
        "Código do curso: "
    )

    curso = None

    for c in dados["cursos"]:

        if c.codigo == codigo_curso:

            curso = c
            break

    if curso is None:

        print(
            "\nCurso não encontrado."
        )

        input(
            "\nEnter para continuar..."
        )

        return

    id_turma = input(
        "ID da turma: "
    )

    semestre = input(
        "Semestre: "
    )

    dia = input(
        "Dia (seg, ter, qua...): "
    )

    horario = input(
        "Horário (08:00-10:00): "
    )

    vagas = int(
        input(
            "Vagas: "
        )
    )

    turma = Turma(
        curso,
        id_turma,
        semestre,
        {
            dia: horario
        },
        vagas
    )

    dados["turmas"].append(
        turma
    )

    salvar_turmas(dados)

    print(
        "\nTurma criada."
    )

    input(
        "\nEnter para continuar..."
    )


def remover_turma(dados):

    turma_id = input(
        "ID da turma: "
    )

    for turma in dados["turmas"]:

        if turma.id == turma_id:

            dados["turmas"].remove(
                turma
            )

            salvar_turmas(dados)

            print(
                "\nTurma removida."
            )

            input(
                "\nEnter para continuar..."
            )

            return

    print(
        "\nTurma não encontrada."
    )

    input(
        "\nEnter para continuar..."
    )


def abrir_turma(dados):

    turma_id = input(
        "ID da turma: "
    )

    for turma in dados["turmas"]:

        if turma.id == turma_id:

            turma.abrir()

            salvar_turmas(dados)

            print(
                "\nTurma aberta."
            )

            input(
                "\nEnter para continuar..."
            )

            return

    print(
        "\nTurma não encontrada."
    )

    input(
        "\nEnter para continuar..."
    )


def fechar_turma(dados):

    turma_id = input(
        "ID da turma: "
    )

    for turma in dados["turmas"]:

        if turma.id == turma_id:

            turma.fechar()

            salvar_turmas(dados)

            print(
                "\nTurma fechada."
            )

            input(
                "\nEnter para continuar..."
            )

            return

    print(
        "\nTurma não encontrada."
    )

    input(
        "\nEnter para continuar..."
    )

# MATRICULAS 

def matricular_aluno(dados):

    matricula_aluno = input(
        "Matrícula do aluno: "
    )

    turma_id = input(
        "ID da turma: "
    )

    aluno = None

    for a in dados["alunos"]:

        if a.matricula == matricula_aluno:

            aluno = a
            break

    turma = None

    for t in dados["turmas"]:

        if t.id == turma_id:

            turma = t
            break

    if aluno is None:

        print("\nAluno não encontrado.")
        return

    if turma is None:

        print("\nTurma não encontrada.")
        return

    try:

        matricula = Matricula(
            aluno,
            turma
        )

        dados["matriculas"].append(
            matricula
        )

        salvar_matriculas(dados)

        print(
            "\nMatrícula realizada."
        )

    except Exception as e:

        print(
            f"\nErro: {e}"
        )

    input(
        "\nEnter para continuar..."
    )
def lancar_nota(dados):

    matricula_aluno = input(
        "Matrícula do aluno: "
    )

    turma_id = input(
        "ID da turma: "
    )

    nota = float(
        input(
            "Nota: "
        )
    )

    for matricula in dados["matriculas"]:

        if (
            matricula.aluno.matricula
            == matricula_aluno
            and
            matricula.turma.id
            == turma_id
        ):

            matricula.lancar_nota(
                nota
            )

            salvar_matriculas(dados)

            print(
                "\nNota lançada."
            )

            input(
                "\nEnter para continuar..."
            )

            return

    print(
        "\nMatrícula não encontrada."
    )

def lancar_frequencia(dados):

    matricula_aluno = input(
        "Matrícula do aluno: "
    )

    turma_id = input(
        "ID da turma: "
    )

    frequencia = float(
        input(
            "Frequência: "
        )
    )

    for matricula in dados["matriculas"]:

        if (
            matricula.aluno.matricula
            == matricula_aluno
            and
            matricula.turma.id
            == turma_id
        ):

            matricula.lancar_frequencia(
                frequencia
            )

            salvar_matriculas(dados)

            print(
                "\nFrequência lançada."
            )

            input(
                "\nEnter para continuar..."
            )

            return

    print(
        "\nMatrícula não encontrada."
    )
def trancar_matricula(dados):

    matricula_aluno = input(
        "Matrícula do aluno: "
    )

    turma_id = input(
        "ID da turma: "
    )

    for matricula in dados["matriculas"]:

        if (
            matricula.aluno.matricula
            == matricula_aluno
            and
            matricula.turma.id
            == turma_id
        ):

            matricula.trancar(
                settings.__dict__
            )

            salvar_matriculas(dados)

            print(
                "\nMatrícula trancada."
            )

            input(
                "\nEnter para continuar..."
            )

            return

    print(
        "\nMatrícula não encontrada."
    )