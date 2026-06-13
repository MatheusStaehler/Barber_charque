# ✂ Barber Charque

Sistema de agendamento online para barbearia, desenvolvido com Flask + MySQL.

## Tecnologias

- Python 3 + Flask
- MySQL
- HTML5, CSS3, JavaScript

## Como executar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/barber-charque.git
cd barber-charque
```

### 2. Crie o ambiente virtual e instale as dependências

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

```bash
# Copie o arquivo de exemplo
copy .env.example .env      # Windows
# cp .env.example .env       # Linux/Mac

# Edite o .env com seus dados do MySQL
```

### 4. Crie o banco de dados

Abra o MySQL Workbench (ou outro cliente) e execute o arquivo `schema.sql`.

Isso cria o banco, as tabelas e um usuário administrador padrão:
- **Telefone:** 51999999999
- **Senha:** admin123

### 5. Execute a aplicação

```bash
python app.py
```

Acesse: [http://localhost:5000](http://localhost:5000)

---

## Estrutura do projeto

```
barber_charque/
├── app.py                  # Aplicação Flask (rotas e lógica)
├── schema.sql              # Script de criação do banco
├── requirements.txt        # Dependências Python
├── Procfile                # Configuração para deploy no Render
├── .env.example            # Exemplo de variáveis de ambiente
├── templates/
│   ├── base.html           # Layout base (navbar, footer, alerts)
│   ├── index.html          # Página inicial
│   ├── login.html          # Login
│   ├── cadastro.html       # Cadastro de cliente
│   ├── dashboard.html      # Agendamentos do cliente
│   ├── agendar.html        # Tela de agendamento
│   ├── admin_dashboard.html# Painel do administrador
│   └── admin_horarios.html # Gerenciar horários disponíveis
└── static/
    └── css/
        └── style.css       # Estilo da aplicação
```

## Deploy no Render

1. Suba o projeto no GitHub.
2. No Render, crie um **Web Service** apontando para o repositório.
3. Configure as variáveis de ambiente (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, SECRET_KEY).
4. Use um banco MySQL externo (ex: PlanetScale, Railway ou Render MySQL).
5. O `Procfile` já configura o Gunicorn automaticamente.

> **Atenção:** adicione `gunicorn` ao `requirements.txt` para o Render.
