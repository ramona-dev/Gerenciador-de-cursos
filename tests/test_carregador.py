import pytest

from persistencia.carregador import carregar_sistema
from persistencia.json_manager import JsonManager


def test_carrega_dados_reais_do_projeto():
    dados = carregar_sistema()
    assert dados["cursos"]
    assert dados["alunos"]
    assert dados["turmas"]
    assert dados["matriculas"]
    ids = [turma.id for turma in dados["turmas"]]
    assert len(ids) == len(set(ids))


def test_carregador_rejeita_ids_de_turma_duplicados(monkeypatch):
    arquivos = {
        "dados/cursos.json": [
            {"codigo": "MAT101", "nome": "Matemática", "carga_horaria": 60, "prerequisitos": []}
        ],
        "dados/alunos.json": [],
        "dados/turmas.json": [
            {"id": "T1", "curso": "MAT101", "semestre": "2026.2", "horarios": {"seg": "08:00-10:00"}, "vagas": 10},
            {"id": "T1", "curso": "MAT101", "semestre": "2026.2", "horarios": {"ter": "08:00-10:00"}, "vagas": 10},
        ],
        "dados/matriculas.json": [],
    }
    monkeypatch.setattr(JsonManager, "carregar", staticmethod(lambda caminho: arquivos[caminho]))
    with pytest.raises(ValueError, match="ID de turma"):
        carregar_sistema()


def test_carregador_rejeita_referencia_de_curso_inexistente(monkeypatch):
    arquivos = {
        "dados/cursos.json": [],
        "dados/alunos.json": [],
        "dados/turmas.json": [
            {"id": "T1", "curso": "MAT101", "semestre": "2026.2", "horarios": {"seg": "08:00-10:00"}, "vagas": 10}
        ],
        "dados/matriculas.json": [],
    }
    monkeypatch.setattr(JsonManager, "carregar", staticmethod(lambda caminho: arquivos[caminho]))
    with pytest.raises(ValueError, match="curso inexistente"):
        carregar_sistema()


def test_matricula_trancada_permanece_trancada_apos_salvar_e_recarregar(
    monkeypatch, tmp_path
):
    import persistencia.json_manager as json_manager
    from modulos.aluno import Aluno
    from modulos.curso import Curso
    from modulos.turma import Turma
    from modulos.matricula import Matricula
    import settings

    monkeypatch.setattr(json_manager, "BASE_DIR", tmp_path)
    curso = Curso("MAT101", "Matemática", 60)
    aluno = Aluno("2026001", "Teste", "teste@email.com")
    turma = Turma(curso, "MAT001", "2026.2", {"seg": "08:00-10:00"}, 10)
    matricula = Matricula(aluno, turma)

    json_manager.JsonManager.salvar("dados/cursos.json", [curso.to_dict()])
    json_manager.JsonManager.salvar("dados/alunos.json", [aluno.to_dict()])
    json_manager.JsonManager.salvar("dados/turmas.json", [turma.to_dict()])
    json_manager.JsonManager.salvar("dados/matriculas.json", [matricula.to_dict()])

    estado = carregar_sistema()
    matricula_carregada = estado["matriculas"][0]
    matricula_carregada.trancar(settings.obter_configuracoes())
    json_manager.JsonManager.salvar(
        "dados/matriculas.json",
        [item.to_dict() for item in estado["matriculas"]],
    )
    json_manager.JsonManager.salvar(
        "dados/alunos.json",
        [item.to_dict() for item in estado["alunos"]],
    )

    estado_recarregado = carregar_sistema()
    matricula_final = estado_recarregado["matriculas"][0]
    aluno_final = estado_recarregado["alunos"][0]
    turma_final = estado_recarregado["turmas"][0]

    assert matricula_final.situacao() == "TRANCADA"
    assert turma_final not in aluno_final.turmas
    assert len(turma_final) == 0
    assert aluno_final.historico == []


def test_carregador_recupera_nota_frequencia_no_historico(monkeypatch):
    from datetime import date
    curso = {"codigo": "MAT101", "nome": "Matemática", "carga_horaria": 60, "prerequisitos": []}
    aluno = {"matricula": "2026001", "nome": "Teste", "email": "teste@email.com", "historico": []}
    turma = {"id": "T1", "curso": "MAT101", "semestre": "2026.2", "horarios": {"seg": "08:00-10:00"}, "vagas": 10, "aberta": True}
    matricula = {"aluno": "2026001", "turma": "T1", "nota": 8.0, "frequencia": 90.0, "ativa": True, "data": date.today().isoformat()}
    arquivos = {
        "dados/cursos.json": [curso], "dados/alunos.json": [aluno],
        "dados/turmas.json": [turma], "dados/matriculas.json": [matricula],
    }
    monkeypatch.setattr(JsonManager, "carregar", staticmethod(lambda caminho: arquivos[caminho]))
    dados = carregar_sistema()
    aluno_carregado = dados["alunos"][0]
    assert aluno_carregado.cr == pytest.approx(8.0)
    assert aluno_carregado.aprovado_em("MAT101")
    assert aluno_carregado.historico[0]["turma"] == "T1"


def test_carregador_rejeita_historico_com_curso_inexistente(monkeypatch):
    arquivos = {
        "dados/cursos.json": [],
        "dados/alunos.json": [{
            "matricula": "2026001", "nome": "Teste", "email": "teste@email.com",
            "historico": [{"curso": "MAT999", "nota": 8.0, "frequencia": 90.0}],
        }],
        "dados/turmas.json": [], "dados/matriculas.json": [],
    }
    monkeypatch.setattr(JsonManager, "carregar", staticmethod(lambda caminho: arquivos[caminho]))
    with pytest.raises(ValueError, match="curso inexistente"):
        carregar_sistema()


def test_carregador_rejeita_historico_vinculado_sem_matricula(monkeypatch):
    arquivos = {
        "dados/cursos.json": [
            {"codigo": "MAT101", "nome": "Matemática", "carga_horaria": 60, "prerequisitos": []}
        ],
        "dados/alunos.json": [{
            "matricula": "2026001", "nome": "Teste", "email": "teste@email.com",
            "historico": [{"curso": "MAT101", "nota": 8.0, "frequencia": 90.0, "turma": "T1"}],
        }],
        "dados/turmas.json": [{
            "id": "T1", "curso": "MAT101", "semestre": "2026.2",
            "horarios": {"seg": "08:00-10:00"}, "vagas": 10, "aberta": True,
        }],
        "dados/matriculas.json": [],
    }
    monkeypatch.setattr(JsonManager, "carregar", staticmethod(lambda caminho: arquivos[caminho]))
    with pytest.raises(ValueError, match="sem matrícula correspondente"):
        carregar_sistema()


def test_carregador_rejeita_matricula_incompleta_com_historico_concluido(monkeypatch):
    arquivos = {
        "dados/cursos.json": [
            {"codigo": "MAT101", "nome": "Matemática", "carga_horaria": 60, "prerequisitos": []}
        ],
        "dados/alunos.json": [{
            "matricula": "2026001", "nome": "Teste", "email": "teste@email.com",
            "historico": [{"curso": "MAT101", "nota": 8.0, "frequencia": 90.0, "turma": "T1"}],
        }],
        "dados/turmas.json": [{
            "id": "T1", "curso": "MAT101", "semestre": "2026.2",
            "horarios": {"seg": "08:00-10:00"}, "vagas": 10, "aberta": True,
        }],
        "dados/matriculas.json": [{
            "aluno": "2026001", "turma": "T1", "nota": None,
            "frequencia": None, "ativa": True, "data": "2026-11-03",
        }],
    }
    monkeypatch.setattr(JsonManager, "carregar", staticmethod(lambda caminho: arquivos[caminho]))
    with pytest.raises(ValueError, match="histórico concluído"):
        carregar_sistema()
