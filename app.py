from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'barber_charque_secret_2024')

# ── Conexão com o banco ───────────────────────────────────────────────────────

def get_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', '3306')),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'barber_charque'),
        ssl_disabled=os.getenv('DB_SSL_DISABLED', 'False') == 'True'
    )

# ── Decorators de autenticação ────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Faça login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Faça login para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        if session.get('tipo') != 'admin':
            flash('Acesso restrito ao administrador.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated

# ── Rotas públicas ────────────────────────────────────────────────────────────

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome     = request.form['nome'].strip()
        telefone = request.form['telefone'].strip()
        senha    = request.form['senha']

        if not nome or not telefone or not senha:
            flash('Preencha todos os campos.', 'danger')
            return render_template('cadastro.html')

        conn = cur = None
        try:
            conn = get_db()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id FROM usuarios WHERE telefone = %s", (telefone,))
            if cur.fetchone():
                flash('Telefone já cadastrado. Faça login.', 'warning')
                return render_template('cadastro.html')

            cur.execute(
                "INSERT INTO usuarios (nome, telefone, senha, tipo) VALUES (%s, %s, %s, 'cliente')",
                (nome, telefone, senha)
            )
            conn.commit()
            flash('Cadastro realizado! Faça login.', 'success')
            return redirect(url_for('login'))
        except Error as e:
            flash(f'Erro ao cadastrar: {e}', 'danger')
        finally:
            if cur: cur.close()
            if conn: conn.close()

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        telefone = request.form['telefone'].strip()
        senha    = request.form['senha']

        conn = cur = None
        try:
            conn = get_db()
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT * FROM usuarios WHERE telefone = %s AND senha = %s",
                (telefone, senha)
            )
            user = cur.fetchone()
            if user:
                session['user_id'] = user['id']
                session['nome']    = user['nome']
                session['tipo']    = user['tipo']
                return redirect(url_for('dashboard'))
            else:
                flash('Telefone ou senha incorretos.', 'danger')
        except Error as e:
            flash(f'Erro ao fazer login: {e}', 'danger')
        finally:
            if cur: cur.close()
            if conn: conn.close()

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))

# ── Dashboard (cliente) ───────────────────────────────────────────────────────

@app.route('/dashboard')
@login_required
def dashboard():
    if session['tipo'] == 'admin':
        return redirect(url_for('admin_dashboard'))

    conn = cur = None
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """SELECT a.id, a.data, a.horario
               FROM agendamentos a
               WHERE a.id_usuario = %s
               ORDER BY a.data, a.horario""",
            (session['user_id'],)
        )
        agendamentos = cur.fetchall()
    except Error as e:
        flash(f'Erro ao carregar agendamentos: {e}', 'danger')
        agendamentos = []
    finally:
        if cur: cur.close()
        if conn: conn.close()

    return render_template('dashboard.html', agendamentos=agendamentos)

# ── Agendamento (cliente) ─────────────────────────────────────────────────────

@app.route('/agendar', methods=['GET', 'POST'])
@login_required
def agendar():
    if session['tipo'] == 'admin':
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        disp_id = request.form.get('disponibilidade_id')
        if not disp_id:
            flash('Selecione um horário.', 'danger')
            return redirect(url_for('agendar'))

        conn = cur = None
        try:
            conn = get_db()
            cur = conn.cursor(dictionary=True)

            # Verifica se o horário ainda existe (não foi reservado por outro)
            cur.execute("SELECT * FROM disponibilidade WHERE id = %s", (disp_id,))
            slot = cur.fetchone()
            if not slot:
                flash('Horário indisponível. Escolha outro.', 'warning')
                return redirect(url_for('agendar'))

            cur.execute(
                "INSERT INTO agendamentos (data, horario, id_usuario) VALUES (%s, %s, %s)",
                (slot['data'], slot['horario'], session['user_id'])
            )
            cur.execute("DELETE FROM disponibilidade WHERE id = %s", (disp_id,))
            conn.commit()
            flash('Agendamento confirmado!', 'success')
            return redirect(url_for('dashboard'))
        except Error as e:
            flash(f'Erro ao agendar: {e}', 'danger')
        finally:
            if cur: cur.close()
            if conn: conn.close()

    # GET – lista horários disponíveis
    conn = cur = None
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM disponibilidade WHERE data >= CURDATE() ORDER BY data, horario"
        )
        slots = cur.fetchall()
    except Error as e:
        flash(f'Erro ao carregar horários: {e}', 'danger')
        slots = []
    finally:
        if cur: cur.close()
        if conn: conn.close()

    return render_template('agendar.html', slots=slots)

@app.route('/cancelar/<int:ag_id>', methods=['POST'])
@login_required
def cancelar(ag_id):
    conn = cur = None
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM agendamentos WHERE id = %s AND id_usuario = %s",
            (ag_id, session['user_id'])
        )
        ag = cur.fetchone()
        if not ag:
            flash('Agendamento não encontrado.', 'danger')
            return redirect(url_for('dashboard'))

        # Devolve o horário à disponibilidade
        cur.execute(
            "INSERT INTO disponibilidade (data, horario) VALUES (%s, %s)",
            (ag['data'], ag['horario'])
        )
        cur.execute("DELETE FROM agendamentos WHERE id = %s", (ag_id,))
        conn.commit()
        flash('Agendamento cancelado. Horário liberado.', 'success')
    except Error as e:
        flash(f'Erro ao cancelar: {e}', 'danger')
    finally:
        if cur: cur.close()
        if conn: conn.close()

    return redirect(url_for('dashboard'))

# ── Painel Admin ──────────────────────────────────────────────────────────────

@app.route('/admin')
@admin_required
def admin_dashboard():
    conn = cur = None
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """SELECT a.id, a.data, a.horario, u.nome, u.telefone
               FROM agendamentos a
               JOIN usuarios u ON u.id = a.id_usuario
               ORDER BY a.data, a.horario"""
        )
        agendamentos = cur.fetchall()
    except Error as e:
        flash(f'Erro: {e}', 'danger')
        agendamentos = []
    finally:
        if cur: cur.close()
        if conn: conn.close()

    return render_template('admin_dashboard.html', agendamentos=agendamentos)

@app.route('/admin/horarios', methods=['GET', 'POST'])
@admin_required
def admin_horarios():
    if request.method == 'POST':
        data    = request.form['data']
        horario = request.form['horario']

        if not data or not horario:
            flash('Preencha data e horário.', 'danger')
            return redirect(url_for('admin_horarios'))

        conn = cur = None
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO disponibilidade (data, horario) VALUES (%s, %s)",
                (data, horario)
            )
            conn.commit()
            flash('Horário cadastrado com sucesso!', 'success')
        except Error as e:
            flash(f'Erro ao cadastrar horário: {e}', 'danger')
        finally:
            if cur: cur.close()
            if conn: conn.close()

        return redirect(url_for('admin_horarios'))

    # GET
    conn = cur = None
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM disponibilidade WHERE data >= CURDATE() ORDER BY data, horario"
        )
        slots = cur.fetchall()
    except Error as e:
        flash(f'Erro: {e}', 'danger')
        slots = []
    finally:
        if cur: cur.close()
        if conn: conn.close()

    return render_template('admin_horarios.html', slots=slots)

@app.route('/admin/horarios/excluir/<int:slot_id>', methods=['POST'])
@admin_required
def admin_excluir_horario(slot_id):
    conn = cur = None
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM disponibilidade WHERE id = %s", (slot_id,))
        conn.commit()
        flash('Horário removido.', 'success')
    except Error as e:
        flash(f'Erro: {e}', 'danger')
    finally:
        if cur: cur.close()
        if conn: conn.close()

    return redirect(url_for('admin_horarios'))

@app.route('/admin/cancelar/<int:ag_id>', methods=['POST'])
@admin_required
def admin_cancelar(ag_id):
    conn = cur = None
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM agendamentos WHERE id = %s", (ag_id,))
        ag = cur.fetchone()
        if ag:
            cur.execute(
                "INSERT INTO disponibilidade (data, horario) VALUES (%s, %s)",
                (ag['data'], ag['horario'])
            )
            cur.execute("DELETE FROM agendamentos WHERE id = %s", (ag_id,))
            conn.commit()
            flash('Agendamento cancelado pelo administrador.', 'success')
    except Error as e:
        flash(f'Erro: {e}', 'danger')
    finally:
        if cur: cur.close()
        if conn: conn.close()

    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)