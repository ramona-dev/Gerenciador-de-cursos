from .pessoa import Pessoa

class Aluno(Pessoa):
    def __init__(self, matricula: str, nome: str, email: str):
        super().__init__(nome, email)  # herda validações de Pessoa
        if not matricula.strip():
            raise ValueError("Matrícula não pode ser vazia.")
        self._matricula = matricula
        self._historico = []   # [{"curso": codigo, "nota": x, "frequencia": y}]
        self._turmas = []      # turmas atuais

    @property
    def matricula(self):
        return self._matricula

    @property
    def historico(self):
        return list(self._historico)

    @property
    def turmas(self):
        return list(self._turmas)

    def adicionar_disciplina(self, curso, nota, frequencia):
        self._historico.append({"curso": curso.codigo, "nota": nota, "frequencia": frequencia})

    def calculo_de_CR(self):
        pass

    def aprovado_em(self):
        pass 