class Curso:
    def __init__(self, codigo: str, nome: str, carga_horaria: int, prerequisitos=None):
        self.codigo = codigo
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.prerequisitos = prerequisitos or []  # lista de códigos de cursos

    def adicionar_prerequisito(self, codigo_pre: str):
        pass
