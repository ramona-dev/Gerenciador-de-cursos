"""Regras de catálogo, unicidade e dependência entre pré-requisitos."""

from modulos.curso import Curso


class CatalogoCursos:
    def __init__(self, cursos=None):
        self._cursos = {}
        for curso in cursos or []:
            self.adicionar_curso(curso)

    @property
    def cursos(self):
        return list(self._cursos.values())

    def buscar(self, codigo):
        return self._cursos.get(str(codigo).strip().upper())

    def adicionar_curso(self, curso):
        if not isinstance(curso, Curso):
            raise TypeError("Objeto deve ser um Curso.")
        if curso.codigo in self._cursos:
            raise ValueError("Código de curso já cadastrado.")
        self._cursos[curso.codigo] = curso

    def remover_curso(self, codigo):
        codigo = str(codigo).strip().upper()
        if codigo not in self._cursos:
            raise ValueError("Curso não encontrado.")
        dependentes = [
            curso.codigo
            for curso in self._cursos.values()
            if codigo in curso.prerequisitos and curso.codigo != codigo
        ]
        if dependentes:
            raise ValueError(
                "Não é possível remover: o curso é pré-requisito de "
                + ", ".join(dependentes)
                + "."
            )
        del self._cursos[codigo]

    def adicionar_prerequisito(self, codigo_curso, codigo_prerequisito):
        codigo_curso = str(codigo_curso).strip().upper()
        codigo_prerequisito = str(codigo_prerequisito).strip().upper()
        curso = self.buscar(codigo_curso)
        if curso is None:
            raise ValueError("Curso não encontrado.")
        if self.buscar(codigo_prerequisito) is None:
            raise ValueError("Pré-requisito inexistente.")
        if self.possui_ciclo(codigo_curso, codigo_prerequisito):
            raise ValueError("Ciclo de pré-requisitos detectado.")
        curso.adicionar_prerequisito(codigo_prerequisito)

    def possui_ciclo(self, codigo_curso, codigo_prerequisito):
        """Verifica se adicionar a aresta curso -> pré-requisito cria um ciclo."""
        visitados = set()

        def dfs(codigo_atual):
            if codigo_atual == codigo_curso:
                return True
            if codigo_atual in visitados:
                return False
            visitados.add(codigo_atual)
            curso_atual = self.buscar(codigo_atual)
            if curso_atual is None:
                return False
            return any(dfs(pre) for pre in curso_atual.prerequisitos)

        return dfs(codigo_prerequisito)

    def validar_referencias(self):
        for curso in self._cursos.values():
            for prerequisito in curso.prerequisitos:
                if prerequisito not in self._cursos:
                    raise ValueError(
                        f"O curso {curso.codigo} possui pré-requisito inexistente: {prerequisito}."
                    )
                if self.possui_ciclo(curso.codigo, prerequisito):
                    raise ValueError(
                        f"Ciclo de pré-requisitos detectado envolvendo {curso.codigo}."
                    )

    def __contains__(self, codigo):
        return str(codigo).strip().upper() in self._cursos

    def __len__(self):
        return len(self._cursos)

    def __iter__(self):
        return iter(self.cursos)

    def __repr__(self):
        return f"CatalogoCursos({len(self)} cursos)"
