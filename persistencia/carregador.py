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


def _mapear_unico(itens, chave, descricao):
    resultado = {}
    for item in itens:
        valor = chave(item)
        if valor in resultado:
            raise ValueError(f"Registro duplicado de {descricao}: {valor!r}.")
        resultado[valor] = item
    return resultado


def carregar_sistema():
    cursos_json = _exigir_lista(JsonManager.carregar("dados/cursos.json"), "cursos")
    alunos_json = _exigir_lista(JsonManager.carregar("dados/alunos.json"), "alunos")
    turmas_json = _exigir_lista(JsonManager.carregar("dados/turmas.json"), "turmas")
    matriculas_json = _exigir_lista(JsonManager.carregar("dados/matriculas.json"), "matriculas")

    cursos = [Curso.from_dict(item) for item in cursos_json]
    cursos_por_codigo = _mapear_unico(cursos, lambda item: item.codigo, "código de curso")
    catalogo = CatalogoCursos(cursos)
    catalogo.validar_referencias()

    alunos = [Aluno.from_dict(item) for item in alunos_json]
    alunos_por_matricula = _mapear_unico(
        alunos, lambda item: item.matricula, "matrícula de aluno"
    )

    turmas = []
    for registro in turmas_json:
        codigo_curso = str(registro.get("curso", "")).strip().upper()
        curso = cursos_por_codigo.get(codigo_curso)
        if curso is None:
            raise ValueError(
                f"A turma {registro.get('id', '?')} referencia o curso inexistente {codigo_curso!r}."
            )
        turmas.append(Turma.from_dict(registro, curso))

    turmas_por_id = _mapear_unico(turmas, lambda item: item.id, "ID de turma")

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
                f"Matrícula do aluno {matricula_aluno} referencia turma inexistente: {id_turma!r}."
            )
        par = (matricula_aluno, id_turma)
        if par in pares_matricula:
            raise ValueError(
                f"Há mais de uma matrícula registrada para o aluno {matricula_aluno} na turma {id_turma}."
            )
        pares_matricula.add(par)
        matriculas.append(Matricula.from_dict(registro, aluno, turma))

    return {
        "cursos": cursos,
        "alunos": alunos,
        "turmas": turmas,
        "matriculas": matriculas,
        "cursos_por_codigo": cursos_por_codigo,
        "alunos_por_matricula": alunos_por_matricula,
        "turmas_por_id": turmas_por_id,
    }
