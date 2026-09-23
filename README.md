# Gerenciador-de-cursos
## 📘 Sistema Academico - README
-----------------------
# Descrição do projeto

O É um sistema acadêmico simples utilizando Orientação a Objetos em Python. O sistema irá representar entidades como Alunos, Cursos, Turmas, Professores e Configurações, fornecendo uma base sólida para gerenciamento de matrículas, cálculo de CR, controle de frequência, requisitos de curso, entre outros.

O foco inicial é estabelecer uma estrutura limpa e modular, com classes bem definidas e responsabilidades claras, seguindo boas práticas de POO

** Objetivo **

O objetivo deste sistema é fornecer uma plataforma simples e eficiente para gestão acadêmica, permitindo que alunos, professores e administradores consultem informações de forma rápida e organizada. O sistema possibilita criar e gerenciar cursos, turmas e matrículas, além de oferecer funcionalidades como lançamento de frequência, acompanhamento das turmas, abertura de novas turmas e visualização dos dados de alunos e professores. A proposta é entregar uma solução robusta, orientada a objetos, focada na lógica de negócios e adequada para uso em linha de comando ou API mínima.

## 📌 Estrutura de Classes e Funções

### 1. Pessoa (`pessoa.py`)
- Classe base para qualquer pessoa no sistema.
- Armazena **nome** e **email**.
- Valida dados.
- Superclasse de `Aluno`.

### 2. Aluno (`aluno.py`)
- Herda de `Pessoa`.
- Armazena **matrícula** e **histórico** de disciplinas.
- Calcula **CR (Coeficiente de Rendimento)**.
- Verifica aprovação em cursos e lista turmas matriculadas.

### 3. Curso (`curso.py`)
- Representa um curso da instituição.
- Guarda **código**, **nome**, **carga horária** e **pré-requisitos**.
- Valida se o aluno pode cursar (pré-requisitos).

### 4. Oferta (`oferta.py`)
- Classe base para ofertas acadêmicas (turmas).
- Armazena **semestre**, **vagas**, **local** e status (aberta/fechada).
- Superclasse de `Turma`.

### 5. Turma (`turma.py`)
- Herda de `Oferta`.
- Representa uma turma específica.
- Controla **curso**, **id da turma**, **horários**, **local** e **matrículas**.
- Valida **choque de horários** e regras de matrícula.

### 6. Matricula (`matricula.py`)
- Representa matrícula de aluno em turma.
- Armazena **aluno**, **turma**, **nota**, **frequência**, **data** e status.
- Métodos para **lançar nota/frequência**, **trancar** e verificar **situação** (CURSANDO/APROVADO/REPROVADO/TRANCADA).

### 7. Relatórios (`relatorios.py`)
- Funções para gerar estatísticas acadêmicas:
  - Alunos por turma.
  - Taxa de aprovação por curso/turma.
  - Distribuição de notas.
  - Alunos em risco.
  - Ranking por CR.

## 🚀 Resumo de Relações
- `Pessoa` → base para `Aluno`.
- `Aluno` ↔ `Matricula` ↔ `Turma`.
- `Curso` → definido em `Turma` e usado para validação de pré-requisitos.
- `Oferta` → base para `Turma`.
- `Relatórios` → funções de análise sem alterar dados.

## 🧬 Como clonar o repositório

## 1️⃣ Pré-requisitos

- Python 3.10 ou superior
- Git

---

## 2️⃣ Clonar o repositório

```bash
git clone https://github.com/ramona-dev/gerenciador-cursos.git
cd gerenciador-cursos

# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate

Rodar o sistema
py main.py

Estrutura UML resumida do sistema
      +---------+
      | Pessoa  |
      +---------+
           ^
           |
       +-------+
       | Aluno |
       +-------+
           |
           | 1..*  (matrículas)
           v
      +-----------+
      | Matricula |
      +-----------+
           |
           | 1       1
           v
        +-------+
        | Turma |
        +-------+
           ^
           |
      +--------+
      | Oferta |
      +--------+

Curso  ----------------> Turma
Relatorios ------------> Aluno / Turma / Matricula
