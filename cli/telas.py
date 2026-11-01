def listar_cursos(dados):

    print("\n=== CURSOS ===")

    for curso in dados["cursos"]:
        print(curso)


def listar_alunos(dados):

    print("\n=== ALUNOS ===")

    for aluno in dados["alunos"]:

        print(
            f"{aluno.matricula}"
            f" - {aluno.nome}"
            f" | CR: {aluno.cr:.2f}"
        )


def listar_turmas(dados):

    print("\n=== TURMAS ===")

    for turma in dados["turmas"]:

        print(
            f"{turma.id}"
            f" - {turma.curso.nome}"
            f" ({len(turma)}/{turma.vagas})"
        )


def listar_matriculas(dados):

    print("\n=== MATRÍCULAS ===")

    for matricula in dados["matriculas"]:

        print(
            f"{matricula.aluno.nome}"
            f" -> {matricula.turma.id}"
            f" -> {matricula.situacao()}"
        )


def relatorio_alunos_por_turma(dados):

    print("\n=== ALUNOS POR TURMA ===")

    for turma in dados["turmas"]:

        print(
            f"\n{turma.id}"
            f" - {turma.curso.nome}"
        )

        for matricula in turma.matriculas:

            print(
                f" - {matricula.aluno.nome}"
            )


def relatorio_top_cr(dados):

    print("\n=== TOP CR ===")

    alunos = sorted(
        dados["alunos"],
        reverse=True
    )

    for posicao, aluno in enumerate(
        alunos[:5],
        start=1
    ):

        print(
            f"{posicao}º "
            f"{aluno.nome}"
            f" - CR {aluno.cr:.2f}"
        )