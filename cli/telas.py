"""Operações interativas da interface de linha de comando."""

import math

import settings
from modulos.aluno import Aluno
from modulos.catalogo_cursos import CatalogoCursos
from modulos.curso import Curso
from modulos.matricula import Matricula
from modulos.oferta import Oferta
from modulos.pessoa import Pessoa
from modulos.turma import Turma, normalizar_dias, parse_horario
from persistencia.json_manager import JsonManager

# Compatibilidade com chamadas antigas: a implementação dos relatórios fica
# exclusivamente em cli/relatorios.py.
from .relatorios import (
    relatorio_alunos_por_turma,
    relatorio_top_cr,
    relatorio_taxa_aprovacao,
    relatorio_distribuicao_notas,
    relatorio_alunos_em_risco,
)


MAX_TENTATIVAS_ENTRADA = 3


# ---------------------------------------------------------------------------
# Utilidades e persistência
# ---------------------------------------------------------------------------

def pausar():
    input("\nPressione Enter para continuar...")


def _executar_com_retentativa(acao, mensagem_sucesso):
    """Executa uma operação; uma regra de negócio inválida encerra a ação."""
    try:
        acao()
        print(f"\n{mensagem_sucesso}")
    except (ValueError, TypeError, KeyError, OSError) as erro:
        print(f"\nErro: {erro}")
    pausar()


def _erro_apos_tentativas(erro, tentativas):
    raise ValueError(
        f"{erro} Operação cancelada após {tentativas} tentativas inválidas."
    ) from erro


def _ler_texto(mensagem, validador=None, max_tentativas=MAX_TENTATIVAS_ENTRADA):
    """Lê texto validado e cancela a operação após tentativas inválidas."""
    for tentativa in range(1, max_tentativas + 1):
        valor = input(mensagem).strip()
        try:
            return validador(valor) if validador else valor
        except (ValueError, TypeError) as erro:
            if tentativa == max_tentativas:
                _erro_apos_tentativas(erro, max_tentativas)
            print(f"\nErro: {erro}")
            print(
                f"Tente novamente ({tentativa + 1}/{max_tentativas})."
            )


def ler_int(mensagem, minimo=None):
    """Lê inteiro dentro do limite informado, com no máximo três tentativas."""
    for tentativa in range(1, MAX_TENTATIVAS_ENTRADA + 1):
        texto = input(mensagem).strip()
        try:
            valor = int(texto)
        except ValueError:
            mensagem_erro = "Digite um número inteiro válido."
        else:
            if minimo is not None and valor < minimo:
                mensagem_erro = (
                    f"Informe um valor maior ou igual a {minimo}."
                )
            else:
                return valor

        if tentativa == MAX_TENTATIVAS_ENTRADA:
            _erro_apos_tentativas(ValueError(mensagem_erro), tentativa)
        print(f"\nErro: {mensagem_erro}")
        print(
            f"Tente novamente ({tentativa + 1}/{MAX_TENTATIVAS_ENTRADA})."
        )


def ler_float(mensagem, minimo=None, maximo=None):
    """Lê decimal finito dentro do intervalo informado, com três tentativas."""
    for tentativa in range(1, MAX_TENTATIVAS_ENTRADA + 1):
        texto = input(mensagem).replace(",", ".").strip()
        try:
            valor = float(texto)
            if not math.isfinite(valor):
                raise ValueError
        except ValueError:
            mensagem_erro = (
                "Digite um número válido dentro do intervalo permitido."
            )
        else:
            if minimo is not None and valor < minimo:
                mensagem_erro = f"O valor mínimo é {minimo}."
            elif maximo is not None and valor > maximo:
                mensagem_erro = f"O valor máximo é {maximo}."
            else:
                return valor

        if tentativa == MAX_TENTATIVAS_ENTRADA:
            _erro_apos_tentativas(ValueError(mensagem_erro), tentativa)
        print(f"\nErro: {mensagem_erro}")
        print(
            f"Tente novamente ({tentativa + 1}/{MAX_TENTATIVAS_ENTRADA})."
        )


def salvar_cursos(dados):
    JsonManager.salvar(
        "dados/cursos.json",
        [curso.to_dict() for curso in dados["cursos"]],
    )
    dados["cursos_por_codigo"] = {
        curso.codigo: curso for curso in dados["cursos"]
    }


def salvar_alunos(dados):
    JsonManager.salvar(
        "dados/alunos.json",
        [aluno.to_dict() for aluno in dados["alunos"]],
    )
    dados["alunos_por_matricula"] = {
        aluno.matricula: aluno for aluno in dados["alunos"]
    }


def salvar_turmas(dados):
    JsonManager.salvar(
        "dados/turmas.json",
        [turma.to_dict() for turma in dados["turmas"]],
    )
    dados["turmas_por_id"] = {
        turma.id: turma for turma in dados["turmas"]
    }


def salvar_matriculas(dados):
    JsonManager.salvar(
        "dados/matriculas.json",
        [matricula.to_dict() for matricula in dados["matriculas"]],
    )


def salvar_resultados_academicos(dados):
    """Persiste matrícula e histórico acadêmico."""
    salvar_matriculas(dados)
    salvar_alunos(dados)


# ---------------------------------------------------------------------------
# Busca e validação
# ---------------------------------------------------------------------------

def _buscar_curso(dados, codigo):
    codigo = str(codigo).strip().upper()
    return next(
        (curso for curso in dados["cursos"] if curso.codigo == codigo),
        None,
    )


def _buscar_aluno(dados, matricula):
    matricula = str(matricula).strip()
    return next(
        (aluno for aluno in dados["alunos"] if aluno.matricula == matricula),
        None,
    )


def _buscar_turma(dados, id_turma):
    id_turma = str(id_turma).strip().upper()
    return next(
        (turma for turma in dados["turmas"] if turma.id == id_turma),
        None,
    )


def _buscar_matricula(dados, matricula_aluno, id_turma):
    matricula_aluno = str(matricula_aluno).strip()
    id_turma = str(id_turma).strip().upper()
    return next(
        (
            item
            for item in dados["matriculas"]
            if item.aluno.matricula == matricula_aluno
            and item.turma.id == id_turma
        ),
        None,
    )
def _validar_formato_matricula(valor):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError("Matrícula não pode ser vazia.")

    matricula = valor.strip()

    if not matricula.isascii() or not matricula.isdecimal():
        raise ValueError(
            "Matrícula deve conter somente números (0 a 9)."
        )

    return matricula

def _validar_codigo_curso(valor):
    return Curso.validar_codigo(valor)


def _ler_codigo_curso(
    dados,
    mensagem="Código do curso: ",
    existente=None,
):
    def validar(valor):
        codigo = _validar_codigo_curso(valor)
        curso = _buscar_curso(dados, codigo)

        if existente is True and curso is None:
            raise ValueError(
                "Curso não encontrado. Informe um código cadastrado."
            )
        if existente is False and curso is not None:
            raise ValueError(
                "Código de curso já cadastrado. Informe outro código."
            )
        return codigo

    return _ler_texto(mensagem, validar)


def _ler_matricula_aluno(
    dados,
    mensagem="Matrícula do aluno: ",
):
    def validar(valor):
        matricula = _validar_formato_matricula(valor)

        if _buscar_aluno(dados, matricula) is None:
            raise ValueError(
                "Aluno não encontrado. "
                "Informe uma matrícula cadastrada."
            )

        return matricula

    return _ler_texto(mensagem, validar)


def _ler_id_turma(dados, mensagem="ID da turma: ", existente=None):
    def validar(valor):
        if not valor:
            raise ValueError("ID da turma não pode ser vazio.")

        identificador = valor.upper()
        turma = _buscar_turma(dados, identificador)
        if existente is True and turma is None:
            raise ValueError(
                "Turma não encontrada. Informe um ID cadastrado."
            )
        if existente is False and turma is not None:
            raise ValueError(
                "Já existe uma turma com esse ID. Informe outro ID."
            )
        return identificador

    return _ler_texto(mensagem, validar)


def _ler_nome(mensagem="Nome: ", validador=None, padrao=None):
    """Lê nome; a regra padrão é a validação de nomes de pessoas."""
    regra = validador or Pessoa.validar_nome

    def validar(valor):
        if not valor and padrao is not None:
            return padrao
        return regra(valor)

    return _ler_texto(mensagem, validar)


def _ler_email(mensagem="E-mail: ", padrao=None):
    def validar(valor):
        if not valor and padrao is not None:
            return padrao
        return Pessoa.validar_email(valor)

    return _ler_texto(mensagem, validar)


def _ler_matricula_existente(dados, exige_ativa=False):
    matricula_aluno = _ler_matricula_aluno(dados)
    id_turma = _ler_id_turma(dados, existente=True)
    item = _buscar_matricula(dados, matricula_aluno, id_turma)

    if item is None:
        raise ValueError(
            "Não existe matrícula desse aluno na turma informada."
        )
    if exige_ativa and not item.ativa:
        raise ValueError(
            "A matrícula está trancada e não aceita novos lançamentos."
        )
    return item


def _normalizar_horario(valor):
    inicio, fim = parse_horario(valor)
    hora_inicio, minuto_inicio = divmod(inicio, 60)
    hora_fim, minuto_fim = divmod(fim, 60)
    return (
        f"{hora_inicio:02d}:{minuto_inicio:02d}-"
        f"{hora_fim:02d}:{minuto_fim:02d}"
    )


def ler_int_opcional(valor, campo, minimo=None):
    """Valida um inteiro recebido no fluxo de edição, com três tentativas."""
    for tentativa in range(1, MAX_TENTATIVAS_ENTRADA + 1):
        try:
            numero = int(valor)
            if minimo is not None and numero < minimo:
                raise ValueError
            return numero
        except ValueError:
            mensagem_erro = (
                f"{campo} deve ser um número inteiro maior ou igual a {minimo}."
            )
            if tentativa == MAX_TENTATIVAS_ENTRADA:
                _erro_apos_tentativas(
                    ValueError(mensagem_erro), tentativa
                )
            print(f"Erro: {mensagem_erro}")
            valor = input(f"Informe novamente {campo}: ").strip()


# ---------------------------------------------------------------------------
# Cursos
# ---------------------------------------------------------------------------

def cadastrar_curso(dados):
    def acao():
        codigo = _ler_codigo_curso(
            dados, "Código: ", existente=False
        )
        nome = _ler_nome(
            "Nome: ",
            validador=Curso.validar_nome,
        )
        carga_horaria = ler_int(
            "Carga horária (horas): ", minimo=1
        )
        ementa = input("Ementa (opcional): ").strip() or None

        curso = Curso(
            codigo,
            nome,
            carga_horaria,
            ementa=ementa,
        )
        CatalogoCursos(dados["cursos"]).adicionar_curso(curso)
        dados["cursos"].append(curso)
        salvar_cursos(dados)

    _executar_com_retentativa(
        acao,
        "Curso cadastrado com sucesso.",
    )


def editar_curso(dados):
    def acao():
        codigo = _ler_codigo_curso(
            dados,
            "Código do curso que deseja editar: ",
            existente=True,
        )
        curso = _buscar_curso(dados, codigo)

        novo_nome = _ler_nome(
            f"Novo nome [{curso.nome}] (Enter mantém): ",
            validador=Curso.validar_nome,
            padrao=curso.nome,
        )
        nova_carga = input(
            f"Nova carga horária [{curso.carga_horaria}] "
            "(Enter mantém): "
        ).strip()
        nova_ementa = input(
            f"Nova ementa [{curso.ementa or 'não informada'}] "
            "(Enter mantém, - remove): "
        ).strip()

        if nova_carga:
            carga_validada = ler_int_opcional(
                nova_carga, "Carga horária", 1
            )
        else:
            carga_validada = curso.carga_horaria

        if nova_ementa == "-":
            ementa_validada = None
        elif nova_ementa:
            ementa_validada = nova_ementa
        else:
            ementa_validada = curso.ementa

        curso_validado = Curso(
            codigo=curso.codigo,
            nome=novo_nome,
            carga_horaria=carga_validada,
            prerequisitos=curso.prerequisitos,
            ementa=ementa_validada,
        )
        curso.nome = curso_validado.nome
        curso.carga_horaria = curso_validado.carga_horaria
        curso.ementa = curso_validado.ementa
        salvar_cursos(dados)

    _executar_com_retentativa(acao, "Curso atualizado.")


def remover_curso(dados):
    def acao():
        codigo = _ler_codigo_curso(
            dados, "Código do curso: ", existente=True
        )
        turmas_vinculadas = [
            turma.id
            for turma in dados["turmas"]
            if turma.curso.codigo == codigo
        ]
        if turmas_vinculadas:
            raise ValueError(
                "Não é possível remover: existem turmas vinculadas ("
                + ", ".join(turmas_vinculadas)
                + ")."
            )

        alunos_com_historico = [
            aluno.matricula
            for aluno in dados["alunos"]
            if any(
                registro.get("curso") == codigo
                for registro in aluno.historico
            )
        ]
        if alunos_com_historico:
            raise ValueError(
                "Não é possível remover: o curso aparece no histórico "
                "dos alunos ("
                + ", ".join(alunos_com_historico)
                + ")."
            )

        CatalogoCursos(dados["cursos"]).remover_curso(codigo)
        dados["cursos"] = [
            curso for curso in dados["cursos"]
            if curso.codigo != codigo
        ]
        salvar_cursos(dados)

    _executar_com_retentativa(acao, "Curso removido.")


def adicionar_prerequisito(dados):
    def acao():
        codigo_curso = _ler_codigo_curso(
            dados, "Código do curso: ", existente=True
        )
        codigo_pre = _ler_codigo_curso(
            dados, "Código do pré-requisito: ", existente=True
        )
        CatalogoCursos(dados["cursos"]).adicionar_prerequisito(
            codigo_curso, codigo_pre
        )
        salvar_cursos(dados)

    _executar_com_retentativa(acao, "Pré-requisito adicionado.")


def remover_prerequisito(dados):
    def acao():
        codigo_curso = _ler_codigo_curso(
            dados, "Código do curso: ", existente=True
        )
        codigo_pre = _ler_codigo_curso(
            dados, "Código do pré-requisito: ", existente=True
        )
        curso = _buscar_curso(dados, codigo_curso)
        curso.remover_prerequisito(codigo_pre)
        salvar_cursos(dados)

    _executar_com_retentativa(acao, "Pré-requisito removido.")


def listar_cursos(dados):
    print("\n=== CURSOS ===")
    if not dados["cursos"]:
        print("Nenhum curso cadastrado.")

    for curso in dados["cursos"]:
        prerequisitos = ", ".join(curso.prerequisitos) or "Nenhum"
        ementa = curso.ementa or "Não informada"
        print(
            f"{curso} | Pré-requisitos: {prerequisitos} | "
            f"Ementa: {ementa}"
        )
    pausar()


# ---------------------------------------------------------------------------
# Alunos
# ---------------------------------------------------------------------------

def cadastrar_aluno(dados):
    def acao():
        def validar_matricula(valor):
            matricula = _validar_formato_matricula(valor)
            if _buscar_aluno(dados, matricula) is not None:
                 raise ValueError(
            "Matrícula já cadastrada. Informe outra matrícula."
        )
            return matricula

        matricula = _ler_texto("Matrícula: ", validar_matricula)
        nome = _ler_nome()
        email = _ler_email()
        aluno = Aluno(matricula, nome, email)
        dados["alunos"].append(aluno)
        salvar_alunos(dados)

    _executar_com_retentativa(acao, "Aluno cadastrado.")


def editar_aluno(dados):
    def acao():
        matricula = _ler_matricula_aluno(
            dados,
            "Matrícula do aluno que deseja editar: ",
        )
        aluno = _buscar_aluno(dados, matricula)
        novo_nome = _ler_nome(
            f"Novo nome [{aluno.nome}] (Enter mantém): ",
            padrao=aluno.nome,
        )
        novo_email = _ler_email(
            f"Novo e-mail [{aluno.email}] (Enter mantém): ",
            padrao=aluno.email,
        )

        aluno_validado = Aluno(
            aluno.matricula,
            novo_nome,
            novo_email,
        )
        aluno.nome = aluno_validado.nome
        aluno.email = aluno_validado.email
        salvar_alunos(dados)

    _executar_com_retentativa(acao, "Aluno atualizado.")


def remover_aluno(dados):
    def acao():
        matricula = _ler_matricula_aluno(dados)
        aluno = _buscar_aluno(dados, matricula)
        possui_registros = any(
            item.aluno.matricula == matricula
            for item in dados["matriculas"]
        )
        if possui_registros:
            raise ValueError(
                "Não é possível remover: o aluno possui matrículas registradas."
            )
        dados["alunos"].remove(aluno)
        salvar_alunos(dados)

    _executar_com_retentativa(acao, "Aluno removido.")


def listar_alunos(dados):
    print("\n=== ALUNOS ===")
    if not dados["alunos"]:
        print("Nenhum aluno cadastrado.")

    for aluno in sorted(
        dados["alunos"],
        key=lambda item: item.nome.casefold(),
    ):
        print(
            f"{aluno.matricula} - {aluno.nome} | "
            f"{aluno.email} | CR: {aluno.cr:.2f}"
        )
    pausar()


# ---------------------------------------------------------------------------
# Turmas
# ---------------------------------------------------------------------------

def criar_turma(dados):
    def acao():
        codigo_curso = _ler_codigo_curso(
            dados, existente=True
        )
        curso = _buscar_curso(dados, codigo_curso)
        id_turma = _ler_id_turma(
            dados, "ID único da turma: ", existente=False
        )
        semestre = _ler_texto(
            "Semestre (ex.: 2026.2): ",
            Oferta.validar_semestre,
        )
        dias = _ler_texto(
            "Dias (ex.: seg qua ou seg,qua): ",
            normalizar_dias,
        )
        horario = _ler_texto(
            "Horário (ex.: 08:00-10:00): ",
            _normalizar_horario,
        )
        vagas = ler_int("Vagas: ", minimo=1)
        local = input("Local (opcional): ").strip()
        dias_horarios = {dia: horario for dia in dias}

        turma = Turma(
            curso,
            id_turma,
            semestre,
            dias_horarios,
            vagas,
            local,
        )
        dados["turmas"].append(turma)
        salvar_turmas(dados)

    _executar_com_retentativa(acao, "Turma criada com sucesso.")


def remover_turma(dados):
    def acao():
        id_turma = _ler_id_turma(dados, existente=True)
        turma = _buscar_turma(dados, id_turma)
        if any(
            item.turma.id == id_turma
            for item in dados["matriculas"]
        ):
            raise ValueError(
                "Não é possível remover: a turma possui matrículas no histórico."
            )
        dados["turmas"].remove(turma)
        salvar_turmas(dados)

    _executar_com_retentativa(acao, "Turma removida.")


def abrir_turma(dados):
    def acao():
        id_turma = _ler_id_turma(dados, existente=True)
        _buscar_turma(dados, id_turma).abrir()
        salvar_turmas(dados)

    _executar_com_retentativa(acao, "Turma aberta.")


def fechar_turma(dados):
    def acao():
        id_turma = _ler_id_turma(dados, existente=True)
        _buscar_turma(dados, id_turma).fechar()
        salvar_turmas(dados)

    _executar_com_retentativa(acao, "Turma fechada.")


def listar_turmas(dados):
    print("\n=== TURMAS ===")
    if not dados["turmas"]:
        print("Nenhuma turma cadastrada.")

    for turma in dados["turmas"]:
        dias = ", ".join(sorted(turma.horarios))
        status = "ABERTA" if turma.aberta else "FECHADA"
        print(
            f"{turma.id} - {turma.curso.nome} | "
            f"Semestre: {turma.semestre} | "
            f"Vagas: {len(turma)}/{turma.vagas} | "
            f"Dias: {dias} | {status}"
        )
    pausar()


# ---------------------------------------------------------------------------
# Matrículas
# ---------------------------------------------------------------------------

def matricular_aluno(dados):
    def acao():
        matricula_aluno = _ler_matricula_aluno(dados)
        id_turma = _ler_id_turma(dados, existente=True)
        existente = _buscar_matricula(
            dados, matricula_aluno, id_turma
        )
        if existente is not None:
            if existente.ativa:
                raise ValueError(
                    "Já existe uma matrícula ativa desse aluno nesta turma."
                )
            raise ValueError(
                "Já existe uma matrícula trancada desse aluno nesta turma. "
                "Não é permitido criar um segundo registro."
            )

        aluno = _buscar_aluno(dados, matricula_aluno)
        turma = _buscar_turma(dados, id_turma)
        matricula = Matricula(aluno, turma)
        dados["matriculas"].append(matricula)
        salvar_matriculas(dados)

    _executar_com_retentativa(
        acao,
        "Matrícula realizada com sucesso.",
    )


def lancar_nota(dados):
    def acao():
        item = _ler_matricula_existente(dados, exige_ativa=True)
        nota = ler_float(
            "Nota (0 a 10): ", minimo=0, maximo=10
        )
        item.lancar_nota(nota)
        salvar_resultados_academicos(dados)

    _executar_com_retentativa(acao, "Nota lançada.")


def lancar_frequencia(dados):
    def acao():
        item = _ler_matricula_existente(dados, exige_ativa=True)
        frequencia = ler_float(
            "Frequência (0 a 100): ", minimo=0, maximo=100
        )
        item.lancar_frequencia(frequencia)
        salvar_resultados_academicos(dados)

    _executar_com_retentativa(acao, "Frequência lançada.")


def trancar_matricula(dados):
    def acao():
        item = _ler_matricula_existente(dados)
        item.trancar(settings.obter_configuracoes())
        salvar_resultados_academicos(dados)

    _executar_com_retentativa(acao, "Matrícula trancada.")


def listar_matriculas(dados):
    print("\n=== MATRÍCULAS ===")
    if not dados["matriculas"]:
        print("Nenhuma matrícula registrada.")

    for item in dados["matriculas"]:
        print(
            f"{item.aluno.matricula} - {item.aluno.nome} -> "
            f"{item.turma.id} ({item.turma.curso.nome}) -> "
            f"{item.situacao()}"
        )
    pausar()
