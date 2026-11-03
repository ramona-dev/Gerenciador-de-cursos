"""Monta o estado do sistema e valida as referências entre arquivos JSON."""

from persistencia.json_manager import JsonManager
from modulos.curso import Curso
from modulos.aluno import Aluno
from modulos.turma import Turma
from modulos.matricula import Matricula
from modulos.catalogo_cursos import CatalogoCursos


def _exigir_lista(dados, arquivo):
    if not isinstance(dados, list):
        raise ValueError(f"O arquivo dados/{arquivo}.json deve conter uma lista JSON.")
    return dados


def _exigir_registros(dados, arquivo):
    for indice, registro in enumerate(dados, start=1):
        if not isinstance(registro, dict):
            raise ValueError(
                f"O registro {indice} de dados/{arquivo}.json deve ser um objeto JSON."
            )
    return dados


def _mapear_unico(itens, chave, descricao):
    resultado = {}
    for item in itens:
        valor = chave(item)
        if valor in resultado:
            raise ValueError(f"Registro duplicado de {descricao}: {valor!r}.")
        resultado[valor] = item
    return resultado


def carregar_sistema():
    cursos_json = _exigir_registros(
        _exigir_lista(JsonManager.carregar("dados/cursos.json"), "cursos"),
        "cursos",
    )
    alunos_json = _exigir_registros(
        _exigir_lista(JsonManager.carregar("dados/alunos.json"), "alunos"),
        "alunos",
    )
    turmas_json = _exigir_registros(
        _exigir_lista(JsonManager.carregar("dados/turmas.json"), "turmas"),
        "turmas",
    )
    matriculas_json = _exigir_registros(
        _exigir_lista(JsonManager.carregar("dados/matriculas.json"), "matriculas"),
        "matriculas",
    )

    cursos = [Curso.from_dict(item) for item in cursos_json]
    cursos_por_codigo = _mapear_unico(
        cursos, lambda item: item.codigo, "código de curso"
    )
    catalogo = CatalogoCursos(cursos)
    catalogo.validar_referencias()

    alunos = [
        Aluno.from_dict(item, codigos_cursos=cursos_por_codigo)
        for item in alunos_json
    ]
    alunos_por_matricula = _mapear_unico(
        alunos, lambda item: item.matricula, "matrícula de aluno"
    )

    turmas = []
    for registro in turmas_json:
        codigo_curso = str(registro.get("curso", "")).strip().upper()
        curso = cursos_por_codigo.get(codigo_curso)
        if curso is None:
            raise ValueError(
                f"A turma {registro.get('id', '?')} referencia o curso "
                f"inexistente {codigo_curso!r}."
            )
        turmas.append(Turma.from_dict(registro, curso))

    turmas_por_id = _mapear_unico(turmas, lambda item: item.id, "ID de turma")

    for aluno in alunos:
        for registro in aluno.historico:
            id_turma = registro.get("turma")
            if id_turma is not None and id_turma not in turmas_por_id:
                raise ValueError(
                    f"O histórico do aluno {aluno.matricula} referencia "
                    f"a turma inexistente {id_turma}."
                )

    matriculas = []
    pares_matricula = set()
    for registro in matriculas_json:
        matricula_aluno = str(registro.get("aluno", "")).strip()
        id_turma = str(registro.get("turma", "")).strip().upper()
        aluno = alunos_por_matricula.get(matricula_aluno)
        turma = turmas_por_id.get(id_turma)
        if aluno is None:
            raise ValueError(
                f"Matrícula referencia aluno inexistente: {matricula_aluno!r}."
            )
        if turma is None:
            raise ValueError(
                f"Matrícula do aluno {matricula_aluno} referencia turma "
                f"inexistente: {id_turma!r}."
            )
        par = (matricula_aluno, id_turma)
        if par in pares_matricula:
            raise ValueError(
                f"Há mais de uma matrícula registrada para o aluno "
                f"{matricula_aluno} na turma {id_turma}."
            )
        pares_matricula.add(par)
        matriculas.append(Matricula.from_dict(registro, aluno, turma))

    # Entradas de histórico vinculadas a uma turma precisam ter uma matrícula
    # correspondente. Registros acadêmicos antigos sem o campo "turma" são
    # preservados como histórico anterior ao controle de matrículas.
    for aluno in alunos:
        historico_por_turma = {
            registro.get("turma"): registro
            for registro in aluno.historico
            if registro.get("turma") is not None
        }
        for id_turma, registro in historico_por_turma.items():
            if (aluno.matricula, id_turma) not in pares_matricula:
                raise ValueError(
                    f"O histórico do aluno {aluno.matricula} possui resultado "
                    f"sem matrícula correspondente na turma {id_turma}."
                )

        for matricula in matriculas:
            if matricula.aluno is not aluno or not matricula.ativa:
                continue
            if (matricula.nota is None or matricula.frequencia is None):
                if matricula.turma.id in historico_por_turma:
                    raise ValueError(
                        f"A matrícula ativa de {aluno.matricula} na turma "
                        f"{matricula.turma.id} possui histórico concluído, mas "
                        "a nota ou a frequência está ausente."
                    )

    return {
        "cursos": cursos,
        "alunos": alunos,
        "turmas": turmas,
        "matriculas": matriculas,
        "cursos_por_codigo": cursos_por_codigo,
        "alunos_por_matricula": alunos_por_matricula,
        "turmas_por_id": turmas_por_id,
    }
