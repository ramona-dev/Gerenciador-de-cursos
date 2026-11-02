from modulos.curso import Curso


class CatalogoCursos:

    def __init__(
        self,
        cursos=None
    ):

        self._cursos = {}

        if cursos:

            for curso in cursos:

                self.adicionar_curso(
                    curso
                )

    @property
    def cursos(self):

        return list(
            self._cursos.values()
        )

    def buscar(
        self,
        codigo
    ):

        return self._cursos.get(
            codigo
        )

    def adicionar_curso(
        self,
        curso
    ):

        if not isinstance(
            curso,
            Curso
        ):
            raise TypeError(
                "Objeto deve ser um Curso."
            )

        if curso.codigo in self._cursos:

            raise ValueError(
                "Código de curso já cadastrado."
            )

        self._cursos[
            curso.codigo
        ] = curso

    def remover_curso(
        self,
        codigo
    ):

        if codigo not in self._cursos:

            raise ValueError(
                "Curso não encontrado."
            )

        del self._cursos[
            codigo
        ]

    def adicionar_prerequisito(
        self,
        codigo_curso,
        codigo_prerequisito
    ):

        curso = self.buscar(
            codigo_curso
        )

        if curso is None:

            raise ValueError(
                "Curso não encontrado."
            )

        prerequisito = self.buscar(
            codigo_prerequisito
        )

        if prerequisito is None:

            raise ValueError(
                "Pré-requisito inexistente."
            )

        if self.possui_ciclo(
            codigo_curso,
            codigo_prerequisito
        ):

            raise ValueError(
                "Ciclo de pré-requisitos detectado."
            )

        curso.adicionar_prerequisito(
            codigo_prerequisito
        )

    def possui_ciclo(
        self,
        codigo_curso,
        codigo_prerequisito
    ):

        visitados = set()

        def dfs(codigo):

            if codigo == codigo_curso:

                return True

            if codigo in visitados:

                return False

            visitados.add(
                codigo
            )

            curso = self.buscar(
                codigo
            )

            if curso is None:

                return False

            for pre in curso.prerequisitos:

                if dfs(pre):

                    return True

            return False

        return dfs(
            codigo_prerequisito
        )

    def __contains__(
        self,
        codigo
    ):

        return (
            codigo
            in self._cursos
        )

    def __len__(self):

        return len(
            self._cursos
        )

    def __iter__(self):

        return iter(
            self.cursos
        )

    def __repr__(self):

        return (
            f"CatalogoCursos("
            f"{len(self)} cursos)"
        )
