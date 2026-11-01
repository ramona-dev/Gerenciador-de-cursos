from persistencia.carregador import carregar_sistema

dados = carregar_sistema()

print(
    len(dados["cursos"])
)

print(
    len(dados["alunos"])
)

print(
    len(dados["turmas"])
)

print(
    len(dados["matriculas"])
)