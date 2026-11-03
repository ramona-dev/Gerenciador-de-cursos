"""Consultas e relatórios acadêmicos, separados da camada de interação."""

import statistics

import settings


SITUACOES_CONCLUIDAS = {
    "APROVADO",
    "REPROVADO_POR_NOTA",
    "REPROVADO_POR_FREQUENCIA",
}


def pausar():
    """Mantém a pausa da interface isolada neste módulo."""
    input("\nPressione Enter para continuar...")


def matriculas_concluidas(matriculas):
    """Retorna apenas matrículas ativas com resultado acadêmico concluído."""
    return [
        matricula
        for matricula in matriculas
        if matricula.ativa and matricula.situacao() in SITUACOES_CONCLUIDAS
    ]


def calcular_resumo_aprovacao(matriculas):
    """Retorna (aprovados, concluidas, taxa_percentual)."""
    concluidas = matriculas_concluidas(matriculas)
    aprovados = sum(
        matricula.situacao() == "APROVADO"
        for matricula in concluidas
    )
    taxa = (aprovados / len(concluidas) * 100) if concluidas else 0.0
    return aprovados, len(concluidas), taxa


def calcular_cr_no_periodo(aluno, periodo, turmas_por_id):
    """Calcula a média simples das notas concluídas do aluno no período.

    Entradas antigas de histórico sem ID de turma não podem ser vinculadas a
    um período letivo e, por isso, não participam deste cálculo.
    """
    notas = []
    for registro in aluno.historico:
        id_turma = registro.get("turma")
        if not id_turma:
            continue

        turma = turmas_por_id.get(id_turma)
        nota = registro.get("nota")
        if turma is None or turma.semestre != periodo or nota is None:
            continue

        notas.append(float(nota))

    if not notas:
        return None
    return statistics.mean(notas)


def _matriculas_da_turma(dados, turma):
    return [
        matricula
        for matricula in dados["matriculas"]
        if matricula.turma.id == turma.id
    ]


def relatorio_alunos_por_turma(dados):
    """Lista alunos ativos por turma e informa ocupação real das vagas."""
    print("\n=== ALUNOS POR TURMA ===")

    if not dados["turmas"]:
        print("Nenhuma turma cadastrada.")
        pausar()
        return

    for turma in sorted(dados["turmas"], key=lambda item: (item.semestre, item.id)):
        matriculas = _matriculas_da_turma(dados, turma)
        ativas = sorted(
            (item for item in matriculas if item.ativa),
            key=lambda item: item.aluno.nome.casefold(),
        )
        trancadas = sum(not item.ativa for item in matriculas)

        print(
            f"\n{turma.id} - {turma.curso.nome} ({turma.semestre}) | "
            f"Ocupação: {len(turma)}/{turma.vagas} vagas"
        )

        if not ativas:
            print("Nenhum aluno com matrícula ativa.")
        else:
            for matricula in ativas:
                print(
                    f" - {matricula.aluno.nome} | "
                    f"{matricula.situacao()}"
                )

        if trancadas:
            print(
                f"Matrículas trancadas: {trancadas} "
                "(não ocupam vagas)."
            )

    pausar()


def _selecionar_periodo(periodos):
    print("\nPeríodos disponíveis:")
    for indice, periodo in enumerate(periodos, start=1):
        print(f"{indice} - {periodo}")

    while True:
        opcao = input("Selecione o período: ").strip()
        try:
            indice = int(opcao)
        except ValueError:
            print("Opção inválida. Digite o número do período.")
            continue

        if 1 <= indice <= len(periodos):
            return periodos[indice - 1]
        print("Opção inválida. Selecione um período listado.")


def relatorio_top_cr(dados):
    """Exibe o Top N pelo CR calculado somente no período escolhido."""
    print("\n=== TOP N ALUNOS POR CR NO PERÍODO ===")
    periodos = sorted({turma.semestre for turma in dados["turmas"]})

    if not periodos:
        print("Não há períodos letivos cadastrados.")
        pausar()
        return

    periodo = _selecionar_periodo(periodos)
    turmas_por_id = {turma.id: turma for turma in dados["turmas"]}
    ranking = []

    for aluno in dados["alunos"]:
        cr_periodo = calcular_cr_no_periodo(aluno, periodo, turmas_por_id)
        if cr_periodo is not None:
            ranking.append((aluno, cr_periodo))

    ranking.sort(key=lambda item: (-item[1], item[0].nome.casefold()))
    ranking = ranking[:settings.top_n_alunos]

    print(f"\nPeríodo: {periodo}")
    if not ranking:
        print("Nenhum aluno possui notas concluídas nesse período.")
    else:
        for posicao, (aluno, cr) in enumerate(ranking, start=1):
            print(f"{posicao}º {aluno.nome} - CR {cr:.2f}")

    pausar()


def relatorio_taxa_aprovacao(dados):
    """Apresenta taxas por curso e por turma, sem contar trancadas/cursando."""
    print("\n=== TAXA DE APROVAÇÃO POR CURSO ===")

    for curso in sorted(dados["cursos"], key=lambda item: item.codigo):
        ids_turmas = {
            turma.id
            for turma in dados["turmas"]
            if turma.curso.codigo == curso.codigo
        }
        matriculas = [
            item
            for item in dados["matriculas"]
            if item.turma.id in ids_turmas
        ]
        aprovados, total, taxa = calcular_resumo_aprovacao(matriculas)
        if total:
            print(f"{curso.codigo} - {curso.nome}: {taxa:.2f}% ({aprovados}/{total})")
        else:
            print(f"{curso.codigo} - {curso.nome}: sem matrículas concluídas")

    print("\n=== TAXA DE APROVAÇÃO POR TURMA ===")
    for turma in sorted(dados["turmas"], key=lambda item: (item.semestre, item.id)):
        aprovados, total, taxa = calcular_resumo_aprovacao(
            _matriculas_da_turma(dados, turma)
        )
        if total:
            print(
                f"{turma.id} - {turma.curso.nome} ({turma.semestre}): "
                f"{taxa:.2f}% ({aprovados}/{total})"
            )
        else:
            print(
                f"{turma.id} - {turma.curso.nome} ({turma.semestre}): "
                "sem matrículas concluídas"
            )

    pausar()


def relatorio_distribuicao_notas(dados):
    """Resume as notas lançadas em matrículas ativas por turma."""
    print("\n=== DISTRIBUIÇÃO DE NOTAS ===")

    for turma in sorted(dados["turmas"], key=lambda item: (item.semestre, item.id)):
        notas = [
            float(item.nota)
            for item in _matriculas_da_turma(dados, turma)
            if item.ativa and item.nota is not None
        ]

        print(f"\nTurma {turma.id} - {turma.curso.nome} ({turma.semestre})")
        if not notas:
            print("Sem notas cadastradas em matrículas ativas.")
            continue

        media = statistics.mean(notas)
        mediana = statistics.median(notas)
        desvio = statistics.stdev(notas) if len(notas) > 1 else 0.0
        print(f"Média: {media:.2f}")
        print(f"Mediana: {mediana:.2f}")
        print(f"Desvio padrão: {desvio:.2f}")

    pausar()


def relatorio_alunos_em_risco(dados):
    """Lista matrículas ativas abaixo dos limites de nota ou frequência."""
    print("\n=== ALUNOS EM RISCO ===")
    encontrados = [
        item
        for item in dados["matriculas"]
        if item.ativa
        and (
            (item.nota is not None and item.nota < settings.nota_minima_aprovacao)
            or (
                item.frequencia is not None
                and item.frequencia < settings.frequencia_minima
            )
        )
    ]

    if not encontrados:
        print("Nenhum aluno em situação de risco.")
    else:
        for item in encontrados:
            print(
                f"{item.aluno.nome} | Turma: {item.turma.id} | "
                f"Nota: {item.nota} | Frequência: {item.frequencia}"
            )

    pausar()
