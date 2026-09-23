# dados.py
import json
from pathlib import Path

# Arquivos de persistência
ARQUIVO = Path("dados.json")
SETTINGS = Path("settings.json")

def salvar_tudo(alunos, cursos, turmas, matriculas):
    """
    Salva todos os dados em dados.json
    """
    dados = {
        "alunos": [
            {
                "matricula": a.matricula,
                "nome": a.nome,
                "email": a.email,
                "historico": a.historico
            }
            for a in alunos
        ],
        "cursos": [
            {
                "codigo": c.codigo,
                "nome": c.nome,
                "carga_horaria": c.carga_horaria,
                "prerequisitos": c.prerequisitos
            }
            for c in cursos
        ],
        "turmas": [
            {
                "id": t.id,
                "curso_codigo": t.curso.codigo,
                "semestre": t.semestre,
                "dias_horarios": t.horarios,
                "vagas": t.vagas,
                "local": getattr(t, "_local", ""),
                "aberta": t.aberta
            }
            for t in turmas
        ],
        "matriculas": [
            {
                "aluno": m.aluno.matricula,
                "turma": m.turma.id,
                "nota": m.nota,
                "frequencia": m.frequencia,
                "ativa": m.ativa,
                "data": str(m.data)
            }
            for m in matriculas
        ]
    }
    ARQUIVO.write_text(json.dumps(dados, indent=4, ensure_ascii=False), encoding="utf-8")


def carregar_tudo():
    """
    Carrega todos os dados de dados.json
    """
    if not ARQUIVO.exists():
        return {"alunos": [], "cursos": [], "turmas": [], "matriculas": []}
    conteudo = ARQUIVO.read_text(encoding="utf-8").strip()
    if not conteudo:
        return {"alunos": [], "cursos": [], "turmas": [], "matriculas": []}
    return json.loads(conteudo)


def carregar_settings():
    """
    Carrega configurações de settings.json ou cria padrão
    """
    if not SETTINGS.exists():
        default = {
            "nota_minima_aprovacao": 6.0,
            "frequencia_minima": 75.0,
            "data_limite_trancamento": "2025-06-30",
            "max_turmas_por_aluno": None,
            "top_n_alunos": 5
        }
        SETTINGS.write_text(json.dumps(default, indent=4), encoding="utf-8")
        return default
    return json.loads(SETTINGS.read_text(encoding="utf-8"))