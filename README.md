# 🎓 csw24-grupoe-T1\_CS-fastapi

## 📑 Índice

* [Descrição](#📘-descrição)
* [Entidades e Banco de Dados](#🧱-entidades-e-banco-de-dados)
* [Arquitetura do Projeto](#🏗️-arquitetura-do-projeto)
* [Especificações Técnicas](#⚙️-especificações-técnicas)
* [Como Executar o Projeto](#▶️-como-executar-o-projeto)
* [Requisitos do Trabalho](#📋-requisitos-do-trabalho)
* [Autores](#👥-autores)

---

## 📘 Descrição

Projeto desenvolvido para o Trabalho 1 da disciplina **Construção de Software**.

---

## 🧱 Entidades e Banco de Dados

### Diagrama Entidade-Relacionamento

![Diagrama Entidade-Relacionamento](diagram-bd.png)

### 📊 Tabelas

| Tabela           | Descrição         |
| ---------------- | ----------------- |
| `Buildings`      | Prédios           |
| `Rooms`          | Salas             |
| `Users`          | Usuários          |
| `Profiles`       | Perfis de acesso  |
| `Disciplines`    | Disciplinas       |
| `Curriculums`    | Currículos        |
| `Classes`        | Turmas            |
| `Evaluations`    | Avaliações        |
| `Lessons`        | Aulas             |
| `Reservations`   | Reservas          |
| `Resources`      | Recursos          |
| `Resource_types` | Tipos de Recursos |

---

## 🏗️ Arquitetura do Projeto

### Estrutura

```
app/
├── __init__.py
├── main.py
├── database.py
├── models/
│   └── resource.py
├── schemas/
│   └── resource.py
├── repositories/
│   └── resource_repository.py
├── services/
│   └── resource_service.py
├── routers/
│   └── resource.py
├── dependencies/
    └── permissions.py
```

### Camadas

* `models/`: Modelos ORM (SQLAlchemy) que definem o banco
* `schemas/`: Modelos de entrada/saída (Pydantic)
* `repositories/`: Acesso ao banco por entidade
* `services/`: Regras de negócio (ex: validação de reservas)
* `routers/`: Endpoints da API REST
* 'dependencies/': Valida permissões de acesso

---

## ⚙️ Especificações Técnicas

* **Framework**: FastAPI
* **Linguagem**: Python
* **Banco de Dados**: MySQL
* **ORM**: SQLAlchemy
* **Documentação**: Swagger UI
* **Empacotamento**: Docker


---

## ▶️ Como Executar o Projeto

1. **Suba os containers**:

```bash
cd t1_cs
docker-compose up --build
```

2. **Acesse a documentação da API**:
   👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📋 Requisitos do Trabalho

### Funcionalidades Esperadas

* Exportar documentação via Swagger
* API funcional com Docker Compose
* Infraestrutura via IaC (opcional)
* Arquitetura desacoplada (dados vs lógica)
* Repositório com nome padrão: `csw24-grupoe-T1_CS-fastapi`
* README com instruções completas de execução

### Permissões por Perfil

| Perfil                 | Permissões                                 |
| -----------------------| ------------------------------------------ |
| Professor (id = 2)     | Editar aulas e reservas                    |
| Coordenador  (id = 3)  | Editar turmas e disciplinas                |
| Administrador (id = 1) | Editar usuários, prédios, salas e recursos |

---

## 👥 Autores

* Henrique Juchem
* Isabela Guerra
* Lucas Wolschick
* Maria Eduarda Maia
* Sofia Batista Sartori

Projeto acadêmico desenvolvido para a disciplina **Construção de Software**.
