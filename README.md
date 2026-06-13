# Barber Charque

## Descrição

O Barber Charque é um sistema web de agendamento para barbearia desenvolvido como Projeto Tecnológico da disciplina de Desenvolvimento de Sistemas. O sistema permite que clientes realizem cadastro, login, agendamento e cancelamento de horários, além de disponibilizar uma área administrativa para gerenciamento dos atendimentos.

## Tecnologias Utilizadas

* Python 3
* Flask
* MySQL
* HTML5
* CSS3

## Instalação e Execução

### 1. Banco de Dados

Criar o banco de dados MySQL:

```sql
CREATE DATABASE barber_charque;
```

Selecionar o banco:

```sql
USE barber_charque;
```

Executar o arquivo `schema.sql` para criar as tabelas necessárias do sistema.

### 2. Configuração

Antes de executar o sistema, é necessário editar o arquivo `.env` e informar os dados de conexão com o banco de dados MySQL.

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

## Credenciais de Teste

### Administrador

Usuário: 123456

Senha: admin

### Cliente

Para acessar como cliente, basta criar uma nova conta através da opção **Cadastro** disponível na página inicial do sistema.

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

## Fluxo de Utilização

### Cliente

1. Acessar a página inicial.
2. Realizar cadastro ou login.
3. Visualizar os horários disponíveis.
4. Selecionar um horário para agendamento.
5. Consultar os agendamentos realizados.
6. Cancelar agendamentos, quando necessário.

### Administrador

1. Realizar login administrativo.
2. Cadastrar novos horários disponíveis.
3. Excluir horários disponíveis.
4. Visualizar todos os agendamentos do sistema.
5. Cancelar agendamentos quando necessário.

## Observação

A Barber Charque trabalha com atendimento simplificado. Todos os serviços possuem valor único de R$ 15,00 e são realizados pelo barbeiro Matheus Staehler. Por esse motivo, o sistema não possui seleção de barbeiro ou de serviços, sendo necessário apenas escolher a data e o horário desejados.

## Estrutura do Projeto

```text
barber_charque/
│
├── app.py
├── schema.sql
├── requirements.txt
├── README.md
├── .env
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
