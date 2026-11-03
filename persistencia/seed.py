"""Gera dados de demonstração nos arquivos JSON (sobrescreve os dados atuais)."""

from modulos.curso import Curso
from modulos.aluno import Aluno
from modulos.turma import Turma
from modulos.matricula import Matricula
from persistencia.json_manager import JsonManager


def gerar_seed():
    mat101 = Curso("MAT101", "Matemática", 60)
    alg101 = Curso("ALG101", "Algoritmos", 60, ["MAT101"])
    poo101 = Curso("POO101", "Programação Orientada a Objetos", 60, ["ALG101"])
    bd101 = Curso("BD101", "Banco de Dados", 60, ["ALG101"])
    es101 = Curso("ES101", "Engenharia de Software", 60, ["POO101"])
    des101 = Curso("DES101", "Design", 60)
    cursos = [mat101, alg101, poo101, bd101, es101, des101]

    maria = Aluno("2025001", "Maria Silva", "maria@email.com")
    joao = Aluno("2025002", "João Souza", "joao@email.com")
    ana = Aluno("2025003", "Ana Lima", "ana@email.com")
    pedro = Aluno("2025004", "Pedro Costa", "pedro@email.com")
    carla = Aluno("2025005", "Carla Santos", "carla@email.com")
    beatriz = Aluno("2025006", "Beatriz Rocha", "beatriz@email.com")
    alunos = [maria, joao, ana, pedro, carla, beatriz]

    for aluno, curso, nota, frequencia in [
        (maria, mat101, 8.5, 90), (maria, alg101, 9.0, 95),
        (joao, mat101, 7.0, 85), (joao, alg101, 7.5, 80),
        (pedro, mat101, 5.0, 90),
        (carla, mat101, 8.0, 90), (carla, alg101, 7.0, 80),
        (beatriz, mat101, 7.5, 85), (beatriz, alg101, 6.5, 75),
    ]:
        aluno.adicionar_disciplina(curso, nota, frequencia)

    turma_poo = Turma(poo101, "TPOO1", "2026.2", {
        "seg": "08:00-10:00", "qua": "08:00-10:00"
    }, 30)
    turma_bd = Turma(bd101, "TBD1", "2026.2", {
        "ter": "10:00-12:00", "qui": "10:00-12:00"
    }, 30)
    turma_es = Turma(es101, "TES1", "2026.2", {"sex": "14:00-18:00"}, 30)
    turma_mat = Turma(mat101, "MAT001", "2026.2", {"seg": "09:00-10:00"}, 45)
    turma_design = Turma(des101, "DES001", "2026.2", {
        "seg": "08:00-10:00", "qua": "08:00-10:00"
    }, 45)
    turmas = [turma_poo, turma_bd, turma_es, turma_mat, turma_design]

    matriculas = []
    for aluno, turma, nota, frequencia in [
        (maria, turma_poo, 9.0, 95),
        (joao, turma_poo, 7.0, 80),
        (carla, turma_bd, None, None),
        (beatriz, turma_bd, 4.0, 85),
    ]:
        matricula = Matricula(aluno, turma)
        if nota is not None:
            matricula.lancar_nota(nota)
        if frequencia is not None:
            matricula.lancar_frequencia(frequencia)
        matriculas.append(matricula)

    for arquivo, registros in [
        ("dados/cursos.json", [item.to_dict() for item in cursos]),
        ("dados/alunos.json", [item.to_dict() for item in alunos]),
        ("dados/turmas.json", [item.to_dict() for item in turmas]),
        ("dados/matriculas.json", [item.to_dict() for item in matriculas]),
    ]:
        JsonManager.salvar(arquivo, registros)

    return {"cursos": cursos, "alunos": alunos, "turmas": turmas, "matriculas": matriculas}


if __name__ == "__main__":
    gerar_seed()
    print("Dados de demonstração gerados. Os JSONs anteriores foram sobrescritos.")
