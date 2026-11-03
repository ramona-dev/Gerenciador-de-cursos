# Gerenciador de Cursos

O Sistema de gerenciamento acadêmico foi desenvolvido em Python, com interface de linha de comando (CLI), persistência de dados em arquivos JSON e aplicação de conceitos de Programação Orientada a Objetos (POO).

Ele permite gerenciar cursos, alunos, turmas e matrículas, além de realizar lançamentos de notas e frequências e gerar relatórios acadêmicos.

---

## 📌 Sobre o projeto

O **Gerenciador de Cursos** foi desenvolvido como um projeto acadêmico com o objetivo de aplicar conceitos de Engenharia de Software e Programação Orientada a Objetos em um sistema funcional.

A aplicação funciona por meio de uma interface de terminal e possui regras para controlar o processo acadêmico, como:

- cadastro, edição, consulta e remoção de cursos;
- cadastro, edição, consulta e remoção de alunos;
- criação e gerenciamento de turmas;
- definição de pré-requisitos entre cursos;
- realização de matrículas;
- validação de pré-requisitos;
- controle de vagas;
- identificação de conflitos de horário;
- controle do limite de turmas por aluno;
- lançamento de notas;
- lançamento de frequência;
- trancamento de matrícula;
- acompanhamento da situação acadêmica;
- geração de relatórios;
- persistência dos dados em arquivos JSON.

---

## 🚀 Funcionalidades

### Cursos

O sistema permite:

- cadastrar cursos;
- listar cursos;
- editar cursos;
- remover cursos;
- adicionar pré-requisitos;
- remover pré-requisitos;
- validar referências entre cursos;
- impedir ciclos de pré-requisitos.

Cada curso possui informações como:

- código;
- nome;
- carga horária;
- pré-requisitos.

---

### Alunos

É possível:

- cadastrar alunos;
- listar alunos;
- editar dados cadastrais;
- remover alunos;
- consultar histórico acadêmico;
- acompanhar o Coeficiente de Rendimento (CR);
- consultar turmas em que o aluno possui matrícula ativa.

O cadastro possui informações como:

- matrícula;
- nome;
- e-mail;
- histórico acadêmico.

---

### Turmas

O sistema permite:

- criar turmas;
- listar turmas;
- abrir uma turma;
- fechar uma turma;
- remover turmas;
- definir período letivo;
- definir horários;
- definir capacidade;
- informar local da turma;
- controlar alunos matriculados.

Também são realizadas validações para evitar conflitos de horário e exceder a capacidade da turma.

---

### Matrículas

O processo de matrícula verifica automaticamente as regras necessárias para que um aluno possa ingressar em uma turma.

Entre as validações estão:

- turma aberta;
- existência de vaga;
- matrícula duplicada;
- pré-requisitos do curso;
- conflitos de horário;
- limite de turmas por aluno.

Após a matrícula, é possível:

- lançar nota;
- lançar frequência;
- consultar situação;
- trancar matrícula.

As situações acadêmicas podem incluir:

- `CURSANDO`;
- `APROVADO`;
- `REPROVADO_POR_NOTA`;
- `REPROVADO_POR_FREQUENCIA`;
- `TRANCADA`.

---

## 📊 Relatórios

O sistema possui relatórios acadêmicos acessíveis pela própria CLI.

### Alunos por turma

Apresenta os alunos vinculados a uma determinada turma.

### Top alunos por CR

Apresenta os alunos com os melhores Coeficientes de Rendimento, considerando a quantidade configurada no sistema.

### Taxa de aprovação

Permite analisar a taxa de aprovação acadêmica.

### Distribuição de notas

Apresenta a distribuição das notas registradas no sistema.

### Alunos em risco

Identifica alunos que apresentam situações acadêmicas que podem indicar risco de reprovação.

---

## 🧠 Regras de negócio

O sistema possui diversas validações para garantir a consistência dos dados.

### Pré-requisitos

Para realizar uma matrícula, o aluno precisa ter sido aprovado em todos os pré-requisitos exigidos pelo curso.

O sistema também impede a criação de ciclos de dependência entre cursos.

Por exemplo:

```text
Curso A → Curso B → Curso C
```

é permitido, mas uma situação como:

```text
Curso A → Curso B → Curso A
```

é bloqueada.

---

### Conflito de horários

Um aluno não pode possuir duas matrículas ativas em turmas que ocorram no mesmo horário.

---

### Capacidade da turma

Uma matrícula somente pode ser realizada quando ainda existir vaga disponível na turma.

---

### Turma aberta

A matrícula somente pode ser realizada em uma turma que esteja aberta para matrícula.

---

### Limite de turmas

O sistema permite configurar uma quantidade máxima de turmas que um aluno pode cursar simultaneamente.

---

### Trancamento

Uma matrícula pode ser trancada respeitando as regras e o prazo configurado para trancamento.

Uma matrícula trancada:

- deixa de ser considerada uma matrícula ativa;
- não ocupa vaga da turma;
- não aparece entre as turmas ativas do aluno;
- mantém seu registro para fins de persistência e histórico.

---

## ⚙️ Configurações

As principais configurações do sistema são armazenadas no arquivo:

```text
settings.json
```

Exemplo:

```json
{
    "nota_minima_aprovacao": 6.0,
    "frequencia_minima": 75.0,
    "data_limite_trancamento": "2027-12-30",
    "max_turmas_por_aluno": null,
    "top_n_alunos": 5
}
```

### Configurações disponíveis

| Configuração | Descrição |
|---|---|
| `nota_minima_aprovacao` | Nota mínima necessária para aprovação |
| `frequencia_minima` | Frequência mínima necessária |
| `data_limite_trancamento` | Data limite para solicitar trancamento |
| `max_turmas_por_aluno` | Limite máximo de turmas por aluno |
| `top_n_alunos` | Quantidade de alunos exibida no ranking de CR |

---

## 💾 Persistência dos dados

Os dados do sistema são armazenados em arquivos JSON.

A pasta `dados/` contém os arquivos utilizados para persistência:

```text
dados/
├── alunos.json
├── cursos.json
├── matriculas.json
└── turmas.json
```

A aplicação realiza a leitura dos arquivos ao iniciar e salva as alterações realizadas durante a utilização do sistema.

A persistência é realizada por meio da classe `JsonManager`, responsável pelas operações de leitura e gravação dos arquivos.

---

## 🏗️ Estrutura do projeto

```text
Gerenciador-de-cursos/
│
├── cli/
│   ├── menu.py
│   └── telas.py
│
├── dados/
│   ├── alunos.json
│   ├── cursos.json
│   ├── matriculas.json
│   └── turmas.json
│
├── modulos/
│   ├── aluno.py
│   ├── catalogo_cursos.py
│   ├── curso.py
│   ├── historico_academico.py
│   ├── matricula.py
│   ├── oferta.py
│   ├── pessoa.py
│   └── turma.py
│
├── persistencia/
│   ├── carregador.py
│   └── json_manager.py
│
├── tests/
│   ├── test_aluno.py
│   ├── test_carregador.py
│   ├── test_cli.py
│   ├── test_curso.py
│   ├── test_matricula.py
│   └── test_turma.py
│
├── main.py
├── settings.py
├── settings.json
└── README.md
```

---

## 🧩 Programação Orientada a Objetos

O projeto foi estruturado utilizando conceitos de Programação Orientada a Objetos.

### Encapsulamento

Os atributos das classes são mantidos encapsulados, utilizando atributos privados e propriedades para controlar o acesso e a alteração dos dados.

Por exemplo:

```python
@property
def nome(self):
    return self._nome
```

As propriedades também permitem realizar validações antes de modificar determinados atributos.

---

### Herança

O sistema utiliza herança para representar relações entre as entidades.

Um exemplo é a classe `Aluno`, que utiliza herança múltipla:

```python
class Aluno(Pessoa, HistoricoAcademico):
```

Dessa forma, o aluno reutiliza comportamentos relacionados aos dados pessoais e ao histórico acadêmico.

---

### Herança múltipla

A classe `Aluno` combina duas responsabilidades:

- `Pessoa`: informações pessoais, como nome e e-mail;
- `HistoricoAcademico`: operações relacionadas ao histórico e ao CR.

Essa estrutura permite aplicar herança múltipla de forma diretamente relacionada ao domínio do sistema.

---

### Métodos especiais

O projeto também utiliza métodos especiais do Python para tornar as classes mais naturais de utilizar.

Entre eles:

```python
__str__
__repr__
__eq__
__lt__
__len__
__contains__
__iter__
```

Esses métodos permitem, por exemplo:

- representar objetos como texto;
- comparar objetos;
- ordenar alunos;
- obter o tamanho de uma turma ou coleção;
- verificar se um elemento pertence a uma coleção;
- iterar sobre objetos.

---

## 🧪 Testes

O projeto utiliza **pytest** para realização dos testes automatizados.

Os testes abrangem diferentes partes do sistema, incluindo:

- alunos;
- cursos;
- turmas;
- matrículas;
- persistência;
- interface CLI;
- regras de negócio.

Para executar todos os testes:

```bash
pytest -q
```

O projeto possui uma suíte de testes automatizados para verificar o funcionamento das principais funcionalidades e regras do sistema.

---

## 📋 Requisitos

Para executar o projeto, é necessário ter instalado:

- Python 3.10 ou superior;
- pip;
- pytest para execução dos testes.

Verifique a instalação do Python com:

```bash
python --version
```

ou:

```bash
python3 --version
```

---

## 📥 Instalação

Clone o repositório:

```bash
git clone https://github.com/ramona-dev/Gerenciador-de-cursos.git
```

Entre na pasta:

```bash
cd Gerenciador-de-cursos
```

Opcionalmente, crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual.

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Instale o pytest:

```bash
pip install pytest
```

---

## ▶️ Executando o sistema

Para iniciar a aplicação:

```bash
python main.py
```

O sistema apresenta o menu principal:

```text
==========================================
 GERENCIADOR DE CURSOS
==========================================
1 - Cursos
2 - Alunos
3 - Turmas
4 - Matrículas
5 - Relatórios
0 - Sair
```

A partir desse menu é possível acessar as funcionalidades do sistema.

---

## 🖥️ Interface

A aplicação utiliza uma interface de linha de comando (CLI), permitindo que o usuário navegue pelas funcionalidades através do terminal.

O menu principal é dividido em cinco áreas:

```text
1 - Cursos
2 - Alunos
3 - Turmas
4 - Matrículas
5 - Relatórios
```

Cada área possui suas próprias operações relacionadas ao domínio acadêmico.

---

## 🔄 Fluxo básico de utilização

Um fluxo típico de utilização do sistema pode ser:

```text
Cadastrar curso
       ↓
Definir pré-requisitos
       ↓
Cadastrar aluno
       ↓
Criar turma
       ↓
Abrir turma
       ↓
Realizar matrícula
       ↓
Lançar nota e frequência
       ↓
Consultar situação acadêmica
       ↓
Gerar relatórios
```

Esse fluxo representa a utilização das principais funcionalidades do sistema.

---

## 📁 Organização das responsabilidades

O projeto foi dividido em módulos para separar as responsabilidades.

### `modulos/`

Contém as principais entidades e regras de domínio do sistema.

### `cli/`

Contém a interface de linha de comando e os menus utilizados pelo usuário.

### `persistencia/`

Responsável pela leitura, gravação e reconstrução dos dados persistidos.

### `dados/`

Armazena os dados persistidos em formato JSON.

### `tests/`

Contém os testes automatizados do sistema.

---

## 🎯 Objetivos acadêmicos

O projeto tem como principais objetivos:

- aplicar Programação Orientada a Objetos;
- utilizar encapsulamento;
- aplicar herança e herança múltipla;
- utilizar métodos especiais do Python;
- implementar regras de negócio;
- trabalhar com persistência de dados;
- desenvolver testes automatizados;
- organizar um sistema em módulos;
- desenvolver uma aplicação funcional utilizando CLI.

---

## 👩‍💻 Responsável

**Ramona Vitória**

Projeto desenvolvido para fins acadêmicos na área de Engenharia de Software.

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos.