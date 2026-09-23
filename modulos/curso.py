class Curso:
    def __init__(self, codigo: str, nome: str, carga_horaria: int, prerequisitos=None):
        if not codigo or len(codigo) < 3:
            raise ValueError("Código do curso deve ter pelo menos 3 caracteres.")
        if not nome.strip():
            raise ValueError("Nome do curso não pode ser vazio.")
        if carga_horaria <= 0:
            raise ValueError("Carga horária deve ser positiva.")

        self.codigo = codigo
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.prerequisitos = prerequisitos or []  # lista de códigos de cursos

    def adicionar_prerequisito(self, codigo_pre: str):
        if codigo_pre == self.codigo:
            raise ValueError("Curso não pode ser pré-requisito de si mesmo.")
        if codigo_pre in self.prerequisitos:
            raise ValueError("Pré-requisito já cadastrado.")
        self.prerequisitos.append(codigo_pre)

    def __str__(self):
        return f"{self.codigo} - {self.nome} ({self.carga_horaria}h)"