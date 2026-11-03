# UML — Gerenciador de Cursos e Alunos

Os diagramas abaixo representam as classes e os fluxos que estão implementados no repositório.

## Diagrama de classes

```mermaid
classDiagram
    class Pessoa {
        -str _nome
        -str _email
        +validar_nome(valor)$
        +validar_email(valor)$
        +nome
        +email
    }

    class HistoricoAcademico {
        -list _historico
        +historico
        +cr
        +calculo_de_CR()
        +adicionar_disciplina()
        +registrar_resultado_matricula()
        +remover_resultado_matricula()
        +aprovado_em()
    }

    class Aluno {
        -str _matricula
        -list _turmas
        +matricula
        +turmas
        +adicionar_turma()
        +remover_turma()
        +to_dict()
        +from_dict()
        +__lt__()
        +__repr__()
    }

    class Oferta {
        -str _semestre
        -int _vagas
        -str _local
        -bool _aberta
        +validar_semestre(valor)$
        +semestre
        +vagas
        +local
        +aberta
        +abrir()
        +fechar()
    }

    class Curso {
        -str _codigo
        -str _nome
        -int _carga_horaria
        -list _prerequisitos
        -str _ementa
        +validar_codigo(valor)$
        +validar_nome(valor)$
        +codigo
        +nome
        +carga_horaria
        +prerequisitos
        +ementa
        +adicionar_prerequisito()
        +remover_prerequisito()
        +to_dict()
        +from_dict()
        +__str__()
        +__repr__()
    }

    class CatalogoCursos {
        -dict _cursos
        +cursos
        +buscar()
        +adicionar_curso()
        +remover_curso()
        +adicionar_prerequisito()
        +possui_ciclo()
        +validar_referencias()
        +__contains__()
        +__len__()
        +__iter__()
        +__repr__()
    }

    class Turma {
        -Curso _curso
        -str _id
        -dict _matriculas
        -dict _horarios
        +curso
        +id
        +horarios
        +matriculas
        +registrar_matricula()
        +tem_choque()
        +adicionar_aluno()
        +__len__()
        +to_dict()
        +from_dict()
    }

    class Matricula {
        -Aluno _aluno
        -Turma _turma
        -float _nota
        -float _frequencia
        -bool _ativa
        -date _data
        +aluno
        +turma
        +nota
        +frequencia
        +ativa
        +data
        +lancar_nota()
        +lancar_frequencia()
        +trancar()
        +situacao()
        +to_dict()
        +from_dict()
        +__eq__()
        +__repr__()
    }

    Aluno --|> Pessoa
    Aluno --|> HistoricoAcademico
    Turma --|> Oferta

    CatalogoCursos "1" o-- "0..*" Curso : administra
    Turma "0..*" --> "1" Curso : oferta
    Turma "1" o-- "0..*" Matricula : registra
    Matricula "0..*" --> "1" Aluno : pertence a
    Matricula "0..*" --> "1" Turma : referencia
    Aluno "1" --> "0..*" Turma : turmas ativas
```

## Diagrama de sequência — matrícula de aluno

```mermaid
sequenceDiagram
    actor Usuario
    participant Menu as cli/menu.py
    participant Tela as cli/telas.py
    participant Matricula
    participant Turma
    participant Aluno
    participant JSON as JsonManager

    Usuario->>Menu: Escolhe Matrículas
    Menu->>Tela: matricular_aluno(dados)
    Tela->>Tela: Localiza aluno e turma
    Tela->>Matricula: Matricula(aluno, turma)
    Matricula->>Turma: adicionar_aluno(aluno, configuracoes)
    Turma->>Aluno: consulta histórico e turmas ativas
    Turma-->>Matricula: validações aprovadas
    Matricula->>Aluno: adicionar_turma(turma)
    Matricula->>Turma: registrar_matricula(self)
    Matricula-->>Tela: objeto de matrícula
    Tela->>JSON: salva dados/matriculas.json
    Tela-->>Usuario: confirma operação
```

## Interpretação

- **Herança múltipla:** `Aluno` herda de `Pessoa` e `HistoricoAcademico`, reunindo dados pessoais e comportamento de histórico/CR.
- **Herança simples:** `Turma` herda de `Oferta`, reutilizando período, capacidade, local e estado de abertura.
- **Catálogo:** `CatalogoCursos` administra cursos e valida unicidade e dependências entre pré-requisitos.
- **Curso:** mantém código, nome, carga horária, lista de pré-requisitos e ementa opcional.
- **Matrícula:** associa um aluno a uma turma e registra nota, frequência, data e estado.
- **Trancamento:** uma matrícula trancada permanece registrada, mas não ocupa vaga nem permanece na coleção de turmas ativas do aluno. O sistema não permite criar um segundo registro para o mesmo aluno e turma.

## Camadas

| Camada | Responsabilidade |
|---|---|
| `main.py` | Inicializa o carregamento dos dados e o menu. |
| `cli/menu.py` | Navegação entre menu principal e submenus. |
| `cli/telas.py` | Entrada de dados, validações de interface e operações CRUD/matrícula. |
| `cli/relatorios.py` | Cálculos e apresentação dos relatórios. |
| `modulos/` | Entidades e regras de negócio do domínio. |
| `persistencia/` | Leitura, gravação e reconstrução dos objetos. |
| `dados/` | Armazenamento em JSON. |
