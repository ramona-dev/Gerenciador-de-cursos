from modulos.curso import Curso
from modulos.aluno import Aluno
from modulos.turma import Turma
from modulos.matricula import Matricula

from persistencia.json_manager import JsonManager


def gerar_seed():

    # -------------------------
    # CURSOS
    # -------------------------

    mat101 = Curso(
        "MAT101",
        "Matemática",
        60
    )

    alg101 = Curso(
        "ALG101",
        "Algoritmos",
        60,
        ["MAT101"]
    )

    poo101 = Curso(
        "POO101",
        "Programação Orientada a Objetos",
        60,
        ["ALG101"]
    )

    bd101 = Curso(
        "BD101",
        "Banco de Dados",
        60,
        ["ALG101"]
    )

    es101 = Curso(
        "ES101",
        "Engenharia de Software",
        60,
        ["POO101"]
    )

    cursos = [
        mat101,
        alg101,
        poo101,
        bd101,
        es101
    ]

    # -------------------------
    # ALUNOS
    # -------------------------

    maria = Aluno(
        "2025001",
        "Maria Silva",
        "maria@email.com"
    )

    joao = Aluno(
        "2025002",
        "João Souza",
        "joao@email.com"
    )

    ana = Aluno(
        "2025003",
        "Ana Lima",
        "ana@email.com"
    )

    pedro = Aluno(
        "2025004",
        "Pedro Costa",
        "pedro@email.com"
    )

    carla = Aluno(
        "2025005",
        "Carla Santos",
        "carla@email.com"
    )

    beatriz = Aluno(
        "2025006",
        "Beatriz Rocha",
        "beatriz@email.com"
    )

    alunos = [
        maria,
        joao,
        ana,
        pedro,
        carla,
        beatriz
    ]

    # -------------------------
    # HISTÓRICOS
    # -------------------------

    maria.adicionar_disciplina(
        mat101,
        8.5,
        90
    )

    maria.adicionar_disciplina(
        alg101,
        9.0,
        95
    )

    joao.adicionar_disciplina(
        mat101,
        7.0,
        85
    )

    joao.adicionar_disciplina(
        alg101,
        7.5,
        80
    )

    pedro.adicionar_disciplina(
        mat101,
        5.0,
        90
    )
    carla.adicionar_disciplina(
    mat101,
    8.0,
    90
)

    carla.adicionar_disciplina(
    alg101,
    7.0,
    80
)
    beatriz.adicionar_disciplina(
    mat101,
    7.5,
    85
)

    beatriz.adicionar_disciplina(
    alg101,
    6.5,
    75
)

    # -------------------------
    # TURMAS
    # -------------------------

    turma_poo = Turma(
        poo101,
        "TPOO1",
        "2026.2",
        {
            "seg": "08:00-10:00",
            "qua": "08:00-10:00"
        },
        vagas=30
    )

    turma_bd = Turma(
        bd101,
        "TBD1",
        "2026.2",
        {
            "ter": "10:00-12:00",
            "qui": "10:00-12:00"
        },
        vagas=30
    )

    turma_es = Turma(
        es101,
        "TES1",
        "2026.2",
        {
            "sex": "14:00-18:00"
        },
        vagas=30
    )

    turmas = [
        turma_poo,
        turma_bd,
        turma_es
    ]

    # -------------------------
    # MATRÍCULAS
    # -------------------------

    matriculas = []

    m1 = Matricula(
        maria,
        turma_poo
    )

    m1.lancar_nota(9.0)
    m1.lancar_frequencia(95)

    matriculas.append(m1)

    m2 = Matricula(
        joao,
        turma_poo
    )

    m2.lancar_nota(7.0)
    m2.lancar_frequencia(80)

    matriculas.append(m2)

    m3 = Matricula(
        carla,
        turma_bd
    )

    matriculas.append(m3)

    m4 = Matricula(
        beatriz,
        turma_bd
    )

    m4.lancar_nota(4.0)
    m4.lancar_frequencia(85)

    matriculas.append(m4)

    # -------------------------
    # SALVAR JSON
    # -------------------------

    JsonManager.salvar(
        "dados/cursos.json",
        [
            curso.to_dict()
            for curso in cursos
        ]
    )

    JsonManager.salvar(
        "dados/alunos.json",
        [
            aluno.to_dict()
            for aluno in alunos
        ]
    )

    JsonManager.salvar(
        "dados/turmas.json",
        [
            turma.to_dict()
            for turma in turmas
        ]
    )

    JsonManager.salvar(
        "dados/matriculas.json",
        [
            matricula.to_dict()
            for matricula in matriculas
        ]
    )

    print(
        "Seed gerado com sucesso."
    )


if __name__ == "__main__":
    gerar_seed()