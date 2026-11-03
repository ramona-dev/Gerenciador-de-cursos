"""Operações da interface de linha de comando."""

import statistics

import settings
from modulos.aluno import Aluno
from modulos.curso import Curso
from modulos.catalogo_cursos import CatalogoCursos
from modulos.matricula import Matricula
from modulos.turma import Turma, normalizar_dias
from persistencia.json_manager import JsonManager


# ---------------------------------------------------------------------------
# Utilidades e persistência
# ---------------------------------------------------------------------------

def pausar():
    input("\nPressione Enter para continuar...")


def ler_int(mensagem, minimo=None):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo is not None and valor < minimo:
                print(f"\nErro: informe um valor maior ou igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("\nErro: digite um número inteiro válido.")


def ler_float(mensagem, minimo=None, maximo=None):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if minimo is not None and valor < minimo:
                print(f"\nErro: o valor mínimo é {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"\nErro: o valor máximo é {maximo}.")
                continue
            return valor
        except ValueError:
            print("\nErro: digite um número válido.")


def salvar_cursos(dados):
    JsonManager.salvar("dados/cursos.json", [curso.to_dict() for curso in dados["cursos"]])
    dados["cursos_por_codigo"] = {curso.codigo: curso for curso in dados["cursos"]}


def salvar_alunos(dados):
    JsonManager.salvar("dados/alunos.json", [aluno.to_dict() for aluno in dados["alunos"]])
    dados["alunos_por_matricula"] = {
        aluno.matricula: aluno for aluno in dados["alunos"]
    }


def salvar_turmas(dados):
    JsonManager.salvar("dados/turmas.json", [turma.to_dict() for turma in dados["turmas"]])
    dados["turmas_por_id"] = {turma.id: turma for turma in dados["turmas"]}


def salvar_matriculas(dados):
    JsonManager.salvar(
        "dados/matriculas.json",
        [matricula.to_dict() for matricula in dados["matriculas"]],
    )


def _buscar_curso(dados, codigo):
    codigo = str(codigo).strip().upper()
    return next((curso for curso in dados["cursos"] if curso.codigo == codigo), None)


def _buscar_aluno(dados, matricula):
    matricula = str(matricula).strip()
    return next((aluno for aluno in dados["alunos"] if aluno.matricula == matricula), None)


def _buscar_turma(dados, id_turma):
    id_turma = str(id_turma).strip().upper()
    return next((turma for turma in dados["turmas"] if turma.id == id_turma), None)


def _buscar_matricula(dados, matricula_aluno, id_turma):
    matricula_aluno = str(matricula_aluno).strip()
    id_turma = str(id_turma).strip().upper()
    return next(
        (
            item for item in dados["matriculas"]
            if item.aluno.matricula == matricula_aluno and item.turma.id == id_turma
        ),
        None,
    )


def _erro_ou_sucesso(acao, mensagem_sucesso):
    try:
        acao()
        print(f"\n{mensagem_sucesso}")
    except (ValueError, TypeError, KeyError) as erro:
        print(f"\nErro: {erro}")
    pausar()


# ---------------------------------------------------------------------------
# Cursos
# ---------------------------------------------------------------------------

def cadastrar_curso(dados):
    print("\n=== CADASTRAR CURSO ===")
    codigo = input("Código: ").strip().upper()
    nome = input("Nome: ").strip()
    carga_horaria = ler_int("Carga horária (horas): ", minimo=1)

    def acao():
        curso = Curso(codigo, nome, carga_horaria)
        catalogo = CatalogoCursos(dados["cursos"])
        catalogo.adicionar_curso(curso)
        dados["cursos"].append(curso)
        salvar_cursos(dados)

    _erro_ou_sucesso(acao, "Curso cadastrado com sucesso.")


def editar_curso(dados):
    codigo = input("Código do curso que deseja editar: ").strip().upper()
    curso = _buscar_curso(dados, codigo)
    if curso is None:
        print("\nCurso não encontrado.")
        pausar()
        return

    novo_nome = input(f"Novo nome [{curso.nome}] (Enter mantém): ").strip()
    nova_carga = input(
        f"Nova carga horária [{curso.carga_horaria}] (Enter mantém): "
    ).strip()

    try:
        nome_validado = novo_nome or curso.nome
        carga_validada = int(nova_carga) if nova_carga else curso.carga_horaria
        curso_validado = Curso(
            curso.codigo,
            nome_validado,
            carga_validada,
            curso.prerequisitos,
        )
        curso.nome = curso_validado.nome
        curso.carga_horaria = curso_validado.carga_horaria
        salvar_cursos(dados)
        print("\nCurso atualizado.")
    except (ValueError, TypeError) as erro:
        print(f"\nErro: {erro}")
    pausar()


def remover_curso(dados):
    codigo = input("Código do curso: ").strip().upper()

    def acao():
        if _buscar_curso(dados, codigo) is None:
            raise ValueError("Curso não encontrado.")
        turmas_vinculadas = [
            turma.id for turma in dados["turmas"]
            if turma.curso.codigo == codigo
        ]
        if turmas_vinculadas:
            raise ValueError(
                "Não é possível remover: existem turmas vinculadas ("
                + ", ".join(turmas_vinculadas) + ")."
            )
        alunos_com_historico = [
            aluno.matricula for aluno in dados["alunos"]
            if any(registro.get("curso") == codigo for registro in aluno.historico)
        ]
        if alunos_com_historico:
            raise ValueError(
                "Não é possível remover: o curso aparece no histórico dos alunos ("
                + ", ".join(alunos_com_historico) + ")."
            )
        catalogo = CatalogoCursos(dados["cursos"])
        catalogo.remover_curso(codigo)
        dados["cursos"] = [curso for curso in dados["cursos"] if curso.codigo != codigo]
        salvar_cursos(dados)

    _erro_ou_sucesso(acao, "Curso removido.")


def adicionar_prerequisito(dados):
    codigo_curso = input("Código do curso: ").strip().upper()
    codigo_pre = input("Código do pré-requisito: ").strip().upper()

    def acao():
        catalogo = CatalogoCursos(dados["cursos"])
        catalogo.adicionar_prerequisito(codigo_curso, codigo_pre)
        salvar_cursos(dados)

    _erro_ou_sucesso(acao, "Pré-requisito adicionado.")


def remover_prerequisito(dados):
    codigo_curso = input("Código do curso: ").strip().upper()
    codigo_pre = input("Código do pré-requisito: ").strip().upper()
    curso = _buscar_curso(dados, codigo_curso)
    if curso is None:
        print("\nCurso não encontrado.")
    else:
        try:
            curso.remover_prerequisito(codigo_pre)
            salvar_cursos(dados)
            print("\nPré-requisito removido.")
        except ValueError as erro:
            print(f"\nErro: {erro}")
    pausar()


def listar_cursos(dados):
    print("\n=== CURSOS ===")
    if not dados["cursos"]:
        print("Nenhum curso cadastrado.")
    for curso in dados["cursos"]:
        prerequisitos = ", ".join(curso.prerequisitos) or "Nenhum"
        print(f"{curso} | Pré-requisitos: {prerequisitos}")
    pausar()


# ---------------------------------------------------------------------------
# Alunos
# ---------------------------------------------------------------------------

def cadastrar_aluno(dados):
    matricula = input("Matrícula: ").strip()
    nome = input("Nome: ").strip()
    email = input("Email: ").strip()

    def acao():
        if _buscar_aluno(dados, matricula) is not None:
            raise ValueError("Matrícula já cadastrada.")
        aluno = Aluno(matricula, nome, email)
        dados["alunos"].append(aluno)
        salvar_alunos(dados)

    _erro_ou_sucesso(acao, "Aluno cadastrado.")


def editar_aluno(dados):
    matricula = input("Matrícula do aluno que deseja editar: ").strip()
    aluno = _buscar_aluno(dados, matricula)
    if aluno is None:
        print("\nAluno não encontrado.")
        pausar()
        return

    novo_nome = input(f"Novo nome [{aluno.nome}] (Enter mantém): ").strip()
    novo_email = input(f"Novo email [{aluno.email}] (Enter mantém): ").strip()
    try:
        aluno_validado = Aluno(
            aluno.matricula,
            novo_nome or aluno.nome,
            novo_email or aluno.email,
        )
        aluno.nome = aluno_validado.nome
        aluno.email = aluno_validado.email
        salvar_alunos(dados)
        print("\nAluno atualizado.")
    except (ValueError, TypeError) as erro:
        print(f"\nErro: {erro}")
    pausar()


def remover_aluno(dados):
    matricula = input("Matrícula do aluno: ").strip()

    def acao():
        aluno = _buscar_aluno(dados, matricula)
        if aluno is None:
            raise ValueError("Aluno não encontrado.")
        possui_registros = any(
            item.aluno.matricula == matricula for item in dados["matriculas"]
        )
        if possui_registros:
            raise ValueError(
                "Não é possível remover: o aluno possui matrículas registradas."
            )
        dados["alunos"].remove(aluno)
        salvar_alunos(dados)

    _erro_ou_sucesso(acao, "Aluno removido.")


def listar_alunos(dados):
    print("\n=== ALUNOS ===")
    if not dados["alunos"]:
        print("Nenhum aluno cadastrado.")
    for aluno in sorted(dados["alunos"], key=lambda item: item.nome.casefold()):
        print(f"{aluno.matricula} - {aluno.nome} | {aluno.email} | CR: {aluno.cr:.2f}")
    pausar()


# ---------------------------------------------------------------------------
# Turmas
# ---------------------------------------------------------------------------

def criar_turma(dados):
    print("\n=== CRIAR TURMA ===")
    codigo_curso = input("Código do curso: ").strip().upper()
    curso = _buscar_curso(dados, codigo_curso)
    if curso is None:
        print("\nCurso não encontrado.")
        pausar()
        return

    id_turma = input("ID único da turma: ").strip().upper()
    if _buscar_turma(dados, id_turma) is not None:
        print("\nErro: já existe uma turma com esse ID. Informe um ID diferente.")
        pausar()
        return

    semestre = input("Semestre (ex.: 2026.2): ").strip()
    dias_digitados = input("Dias (ex.: seg qua ou seg,qua): ").strip()
    horario = input("Horário (ex.: 08:00-10:00): ").strip()
    vagas = ler_int("Vagas: ", minimo=1)
    local = input("Local (opcional): ").strip()

    try:
        dias = normalizar_dias(dias_digitados)
        dias_horarios = {dia: horario for dia in dias}
        turma = Turma(curso, id_turma, semestre, dias_horarios, vagas, local)
        dados["turmas"].append(turma)
        salvar_turmas(dados)
        print("\nTurma criada com sucesso.")
    except (ValueError, TypeError) as erro:
        print(f"\nErro: {erro}")
    pausar()


def remover_turma(dados):
    id_turma = input("ID da turma: ").strip().upper()

    def acao():
        turma = _buscar_turma(dados, id_turma)
        if turma is None:
            raise ValueError("Turma não encontrada.")
        if any(item.turma.id == id_turma for item in dados["matriculas"]):
            raise ValueError(
                "Não é possível remover: a turma possui matrículas no histórico."
            )
        dados["turmas"].remove(turma)
        salvar_turmas(dados)

    _erro_ou_sucesso(acao, "Turma removida.")


def abrir_turma(dados):
    id_turma = input("ID da turma: ").strip().upper()
    turma = _buscar_turma(dados, id_turma)
    if turma is None:
        print("\nTurma não encontrada.")
    else:
        turma.abrir()
        salvar_turmas(dados)
        print("\nTurma aberta.")
    pausar()


def fechar_turma(dados):
    id_turma = input("ID da turma: ").strip().upper()
    turma = _buscar_turma(dados, id_turma)
    if turma is None:
        print("\nTurma não encontrada.")
    else:
        turma.fechar()
        salvar_turmas(dados)
        print("\nTurma fechada.")
    pausar()


def listar_turmas(dados):
    print("\n=== TURMAS ===")
    if not dados["turmas"]:
        print("Nenhuma turma cadastrada.")
    for turma in dados["turmas"]:
        dias = ", ".join(sorted(turma.horarios))
        status = "ABERTA" if turma.aberta else "FECHADA"
        print(
            f"{turma.id} - {turma.curso.nome} | Semestre: {turma.semestre} "
            f"| Vagas: {len(turma)}/{turma.vagas} | Dias: {dias} | {status}"
        )
    pausar()


# ---------------------------------------------------------------------------
# Matrículas
# ---------------------------------------------------------------------------

def matricular_aluno(dados):
    matricula_aluno = input("Matrícula do aluno: ").strip()
    id_turma = input("ID da turma: ").strip().upper()
    aluno = _buscar_aluno(dados, matricula_aluno)
    turma = _buscar_turma(dados, id_turma)

    if aluno is None:
        print("\nAluno não encontrado.")
        pausar()
        return
    if turma is None:
        print("\nTurma não encontrada.")
        pausar()
        return
    if _buscar_matricula(dados, matricula_aluno, id_turma) is not None:
        print("\nErro: já existe um registro de matrícula para esse aluno e turma.")
        pausar()
        return

    try:
        matricula = Matricula(aluno, turma)
        dados["matriculas"].append(matricula)
        salvar_matriculas(dados)
        print("\nMatrícula realizada com sucesso.")
    except (ValueError, TypeError) as erro:
        print(f"\nErro: {erro}")
    pausar()


def lancar_nota(dados):
    matricula_aluno = input("Matrícula do aluno: ").strip()
    id_turma = input("ID da turma: ").strip().upper()
    item = _buscar_matricula(dados, matricula_aluno, id_turma)
    if item is None:
        print("\nMatrícula não encontrada.")
        pausar()
        return
    nota = ler_float("Nota (0 a 10): ", minimo=0, maximo=10)
    try:
        item.lancar_nota(nota)
        salvar_matriculas(dados)
        print("\nNota lançada.")
    except ValueError as erro:
        print(f"\nErro: {erro}")
    pausar()


def lancar_frequencia(dados):
    matricula_aluno = input("Matrícula do aluno: ").strip()
    id_turma = input("ID da turma: ").strip().upper()
    item = _buscar_matricula(dados, matricula_aluno, id_turma)
    if item is None:
        print("\nMatrícula não encontrada.")
        pausar()
        return
    frequencia = ler_float("Frequência (0 a 100): ", minimo=0, maximo=100)
    try:
        item.lancar_frequencia(frequencia)
        salvar_matriculas(dados)
        print("\nFrequência lançada.")
    except ValueError as erro:
        print(f"\nErro: {erro}")
    pausar()


def trancar_matricula(dados):
    matricula_aluno = input("Matrícula do aluno: ").strip()
    id_turma = input("ID da turma: ").strip().upper()
    item = _buscar_matricula(dados, matricula_aluno, id_turma)
    if item is None:
        print("\nMatrícula não encontrada.")
    else:
        try:
            item.trancar(settings.obter_configuracoes())
            salvar_matriculas(dados)
            print("\nMatrícula trancada.")
        except ValueError as erro:
            print(f"\nErro: {erro}")
    pausar()


def listar_matriculas(dados):
    print("\n=== MATRÍCULAS ===")
    if not dados["matriculas"]:
        print("Nenhuma matrícula registrada.")
    for item in dados["matriculas"]:
        print(
            f"{item.aluno.matricula} - {item.aluno.nome} -> "
            f"{item.turma.id} ({item.turma.curso.nome}) -> {item.situacao()}"
        )
    pausar()


# ---------------------------------------------------------------------------
# Relatórios
# ---------------------------------------------------------------------------

def relatorio_alunos_por_turma(dados):
    print("\n=== ALUNOS POR TURMA ===")
    for turma in dados["turmas"]:
        print(f"\n{turma.id} - {turma.curso.nome} ({turma.semestre})")
        matriculas = [item for item in dados["matriculas"] if item.turma.id == turma.id]
        if not matriculas:
            print("Nenhum aluno matriculado.")
            continue
        for item in matriculas:
            print(f" - {item.aluno.nome} | {item.situacao()}")
    pausar()


def relatorio_top_cr(dados):
    print("\n=== TOP ALUNOS POR CR ===")
    top_n = settings.top_n_alunos
    alunos = sorted(dados["alunos"], reverse=True)[:top_n]
    if not alunos:
        print("Nenhum aluno cadastrado.")
    for posicao, aluno in enumerate(alunos, start=1):
        print(f"{posicao}º {aluno.nome} - CR {aluno.cr:.2f}")
    pausar()


def relatorio_taxa_aprovacao(dados):
    print("\n=== TAXA DE APROVAÇÃO POR TURMA ===")
    for turma in dados["turmas"]:
        concluidas = [
            item for item in dados["matriculas"]
            if item.turma.id == turma.id
            and item.situacao() in {"APROVADO", "REPROVADO_POR_NOTA", "REPROVADO_POR_FREQUENCIA"}
        ]
        aprovados = sum(1 for item in concluidas if item.situacao() == "APROVADO")
        taxa = (aprovados / len(concluidas) * 100) if concluidas else 0.0
        print(f"{turma.id} - {turma.curso.nome}: {taxa:.2f}% ({aprovados}/{len(concluidas)})")
    pausar()


def relatorio_distribuicao_notas(dados):
    print("\n=== DISTRIBUIÇÃO DE NOTAS ===")
    for turma in dados["turmas"]:
        notas = [
            float(item.nota) for item in dados["matriculas"]
            if item.turma.id == turma.id and item.nota is not None and item.ativa
        ]
        print(f"\nTurma {turma.id} - {turma.curso.nome}")
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
    print("\n=== ALUNOS EM RISCO ===")
    encontrados = [
        item for item in dados["matriculas"]
        if item.ativa and (
            (item.nota is not None and item.nota < settings.nota_minima_aprovacao)
            or (item.frequencia is not None and item.frequencia < settings.frequencia_minima)
        )
    ]
    if not encontrados:
        print("Nenhum aluno em situação de risco.")
    for item in encontrados:
        print(
            f"{item.aluno.nome} | Turma: {item.turma.id} "
            f"| Nota: {item.nota} | Frequência: {item.frequencia}"
        )
    pausar()
