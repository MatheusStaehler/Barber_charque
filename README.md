# ✂ Barber Charque# Barber Charque

## Descrição do Sistema

O Barber Charque é um sistema web desenvolvido para auxiliar no gerenciamento de agendamentos de uma barbearia. A aplicação permite que clientes realizem cadastro, efetuem login e agendem horários disponíveis. Além disso, o sistema possui uma área administrativa para gerenciamento dos horários e acompanhamento dos agendamentos realizados.

## Tecnologias Utilizadas

* Python 3
* Flask
* MySQL
* HTML5
* CSS3

## Instalação e Execução

### 1. Banco de Dados

Criar o banco de dados:

```sql
CREATE DATABASE barber_charque;
```

Selecionar o banco:

```sql
USE barber_charque;
```

Executar o script disponível no arquivo `schema.sql` para criação das tabelas do sistema.

### 2. Configuração

Renomear o arquivo `.env.example` para `.env` e configurar os dados de conexão com o banco de dados.

Exemplo:

```text
SECRET_KEY=sua_chave_secreta

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=barber_charque
```

### 3. Instalação das Dependências

Executar o comando:

```bash
pip install -r requirements.txt
```

### 4. Inicialização do Sistema

Executar:

```bash
python app.py
```

Após a execução, acessar:

```text
http://127.0.0.1:5000
```

## Funcionalidades

### Cliente

* Cadastro de usuário
* Login no sistema
* Visualização dos horários disponíveis
* Agendamento de horários
* Cancelamento de agendamentos

### Administrador

* Login administrativo
* Cadastro de horários disponíveis
* Exclusão de horários disponíveis
* Visualização de todos os agendamentos
* Cancelamento de agendamentos

## Estrutura do Projeto

```text
barber_charque/
│
├── app.py
├── schema.sql
├── requirements.txt
├── .env.example
├── static/
│   └── css/
│       └── style.css
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── cadastro.html
    ├── dashboard.html
    ├── agendar.html
    ├── admin_dashboard.html
    └── admin_horarios.html
```

## Desenvolvedor

Matheus Bauer Staehler Nunes

Curso de Análise e Desenvolvimento de Sistemas – ULBRA
