from persistencia.json_manager import JsonManager

from modulos.curso import Curso
from modulos.aluno import Aluno
from modulos.turma import Turma
from modulos.matricula import Matricula


def carregar_sistema():

    # -------------------------
    # CURSOS
    # -------------------------

    cursos_json = JsonManager.carregar(
        "dados/cursos.json"
    )

    cursos = [
        Curso.from_dict(curso)
        for curso in cursos_json
    ]

    cursos_por_codigo = {
        curso.codigo: curso
        for curso in cursos
    }

    # -------------------------
    # ALUNOS
    # -------------------------

    alunos_json = JsonManager.carregar(
        "dados/alunos.json"
    )

    alunos = [
        Aluno.from_dict(aluno)
        for aluno in alunos_json
    ]

    alunos_por_matricula = {
        aluno.matricula: aluno
        for aluno in alunos
    }

    # -------------------------
    # TURMAS
    # -------------------------

    turmas_json = JsonManager.carregar(
        "dados/turmas.json"
    )

    turmas = []

    for dados in turmas_json:

        curso = cursos_por_codigo[
            dados["curso"]
        ]

        turma = Turma.from_dict(
            dados,
            curso
        )

        turmas.append(
            turma
        )

    turmas_por_id = {
        turma.id: turma
        for turma in turmas
    }

    # -------------------------
    # MATRÍCULAS
    # -------------------------

    matriculas_json = JsonManager.carregar(
        "dados/matriculas.json"
    )

    matriculas = []

    for dados in matriculas_json:

        aluno = alunos_por_matricula[
            dados["aluno"]
        ]

        turma = turmas_por_id[
            dados["turma"]
        ]

        matricula = Matricula.from_dict(
            dados,
            aluno,
            turma
        )

        matriculas.append(
            matricula
        )

    return {
        "cursos": cursos,
        "alunos": alunos,
        "turmas": turmas,
        "matriculas": matriculas,
        "cursos_por_codigo": cursos_por_codigo,
        "alunos_por_matricula": alunos_por_matricula,
        "turmas_por_id": turmas_por_id
    }