from cli import telas
from modulos.aluno import Aluno
from modulos.curso import Curso
from modulos.matricula import Matricula
from modulos.turma import Turma
import persistencia.json_manager as json_manager


def dados_basicos():
    curso = Curso("MAT101", "Matemática", 60)
    aluno = Aluno("2026001", "Teste", "teste@email.com")
    turma = Turma(curso, "MAT001", "2026.2", {"seg": "08:00-10:00"}, 10)
    return {
        "cursos": [curso],
        "alunos": [aluno],
        "turmas": [turma],
        "matriculas": [],
    }


def configurar_input(monkeypatch, valores):
    iterator = iter(valores)
    monkeypatch.setattr("builtins.input", lambda _mensagem="": next(iterator))
    monkeypatch.setattr(telas, "pausar", lambda: None)


def test_criar_turma_rejeita_id_duplicado(monkeypatch, capsys):
    dados = dados_basicos()
    configurar_input(monkeypatch, ["MAT101", "MAT001"])
    telas.criar_turma(dados)
    assert len(dados["turmas"]) == 1
    assert "ID" in capsys.readouterr().out


def test_criar_turma_separa_dias_informados(monkeypatch, tmp_path):
    dados = dados_basicos()
    monkeypatch.setattr(json_manager, "BASE_DIR", tmp_path)
    configurar_input(monkeypatch, ["MAT101", "MAT002", "2026.2", "ter qui", "10:00-12:00", "15", "Bloco A"])
    telas.criar_turma(dados)
    nova = dados["turmas"][-1]
    assert nova.id == "MAT002"
    assert set(nova.horarios) == {"ter", "qui"}
    assert nova.vagas == 15


def test_remover_aluno_bloqueia_aluno_com_matricula(monkeypatch, capsys):
    dados = dados_basicos()
    matricula = Matricula(dados["alunos"][0], dados["turmas"][0])
    dados["matriculas"].append(matricula)
    configurar_input(monkeypatch, ["2026001"])
    telas.remover_aluno(dados)
    assert len(dados["alunos"]) == 1
    assert "possui matrículas" in capsys.readouterr().out


def test_cli_nao_lanca_frequencia_em_matricula_trancada(monkeypatch, capsys):
    dados = dados_basicos()
    matricula = Matricula(dados["alunos"][0], dados["turmas"][0])
    import settings
    matricula.trancar(settings.obter_configuracoes())
    dados["matriculas"].append(matricula)
    configurar_input(monkeypatch, ["2026001", "MAT001", "80"])
    telas.lancar_frequencia(dados)
    saida = capsys.readouterr().out
    assert "Não é possível lançar frequência" in saida
    assert matricula.frequencia is None
