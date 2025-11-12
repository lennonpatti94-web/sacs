# ==========================================================
# Projeto: SACS - Sistema de Agendamento de Consultas
# Autor: Lennon Patti
# Descrição: Sistema em Flask com autenticação, controle de acesso
# e gerenciamento de pacientes, consultas, profissionais e usuários.
# ==========================================================

from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import os

# ---------------- CONFIGURAÇÃO GERAL ----------------
app = Flask(__name__)
app.secret_key = 'sacs_secret_key'  # chave para sessões Flask

# Configuração do banco de dados
DB_HOST = os.environ.get('SACS_DB_HOST', 'localhost')
DB_USER = os.environ.get('SACS_DB_USER', 'sacs_user')
DB_PASS = os.environ.get('SACS_DB_PASS', '1234')
DB_NAME = os.environ.get('SACS_DB_NAME', 'sacs_db')

def get_db_connection():
    """Retorna uma conexão com o banco MySQL."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# ---------------- LOGIN E AUTENTICAÇÃO ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Tela de login de usuários."""
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE email=%s AND senha=%s", (email, senha))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['usuario_id'] = user['id']
            session['usuario_nome'] = user['nome']
            session['perfil'] = user['perfil']
            flash(f"Bem-vindo(a), {user['nome']}!", "success")
            return redirect(url_for('index'))
        else:
            flash("E-mail ou senha inválidos!", "danger")
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Finaliza a sessão do usuário."""
    session.clear()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for('login'))


# ---------------- PROTEÇÃO DE ROTAS ----------------

from functools import wraps

def login_required(func):
    """Decorator para proteger rotas que exigem login."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'usuario_id' not in session:
            flash("Por favor, faça login primeiro!", "warning")
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper


# ---------------- PÁGINA INICIAL ----------------

@app.route('/')
@login_required
def index():
    """Tela inicial que lista pacientes."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM paciente ORDER BY nome")
    pacientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', pacientes=pacientes, usuario=session.get('usuario_nome'))


# ---------------- CONSULTAS ----------------

@app.route('/consultas')
@login_required
def listar_consultas():
    """Lista as consultas agendadas."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id, p.nome AS paciente, pr.nome AS profissional, c.data_hora, c.status
        FROM consulta c
        JOIN paciente p ON c.paciente_id = p.id
        JOIN profissional pr ON c.profissional_id = pr.id
        ORDER BY c.data_hora DESC
    """)
    consultas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('consultas.html', consultas=consultas)
# ---------------- AGENDAR CONSULTA ----------------

@app.route('/agendar', methods=['GET', 'POST'])
@login_required
def agendar_consulta():
    """Permite agendar uma nova consulta."""
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        paciente_id = request.form['paciente_id']
        profissional_id = request.form['profissional_id']
        data_hora = request.form['data_hora']

        if not paciente_id or not profissional_id or not data_hora:
            flash("Preencha todos os campos!", "danger")
        else:
            cursor.execute("""
                INSERT INTO consulta (paciente_id, profissional_id, data_hora, status)
                VALUES (%s, %s, %s, %s)
            """, (paciente_id, profissional_id, data_hora, 'Agendada'))
            conn.commit()
            flash("Consulta agendada com sucesso!", "success")
            cursor.close()
            conn.close()
            return redirect(url_for('listar_consultas'))

    # Carrega pacientes e profissionais para o formulário
    cursor.execute("SELECT id, nome FROM paciente ORDER BY nome")
    pacientes = cursor.fetchall()

    cursor.execute("SELECT id, nome FROM profissional ORDER BY nome")
    profissionais = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('agendar.html', pacientes=pacientes, profissionais=profissionais)


# ---------------- PROFISSIONAIS (somente ADMIN) ----------------

@app.route('/profissionais', methods=['GET', 'POST'])
@login_required
def profissionais():
    """Permite ao administrador cadastrar e listar profissionais."""
    if session.get('perfil') != 'admin':
        flash("Acesso negado! Somente o administrador pode cadastrar profissionais.", "danger")
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        especialidade = request.form['especialidade']
        cursor.execute("INSERT INTO profissional (nome, especialidade) VALUES (%s, %s)", (nome, especialidade))
        conn.commit()
        flash("Profissional cadastrado com sucesso!", "success")

    cursor.execute("SELECT * FROM profissional ORDER BY nome")
    lista = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('profissionais.html', profissionais=lista)


# ---------------- USUÁRIOS (somente ADMIN) ----------------

@app.route('/usuarios', methods=['GET', 'POST'])
@login_required
def usuarios():
    """Permite ao administrador cadastrar e listar usuários do sistema."""
    if session.get('perfil') != 'admin':
        flash("Acesso negado! Somente o administrador pode cadastrar usuários.", "danger")
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        perfil = request.form['perfil']

        cursor.execute("""
            INSERT INTO usuario (nome, email, senha, perfil)
            VALUES (%s, %s, %s, %s)
        """, (nome, email, senha, perfil))
        conn.commit()
        flash("Usuário cadastrado com sucesso!", "success")

    cursor.execute("SELECT id, nome, email, perfil FROM usuario ORDER BY nome")
    lista = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('usuarios.html', usuarios=lista)

# ---------------- CADASTRO DE PACIENTES ----------------

@app.route('/pacientes', methods=['GET', 'POST'])
@login_required
def pacientes():
    """Permite cadastrar e listar pacientes."""
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']

        if not nome or not telefone:
            flash("Preencha todos os campos!", "danger")
        else:
            cursor.execute("INSERT INTO paciente (nome, telefone) VALUES (%s, %s)", (nome, telefone))
            conn.commit()
            flash("Paciente cadastrado com sucesso!", "success")

    cursor.execute("SELECT * FROM paciente ORDER BY nome")
    lista = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('pacientes.html', pacientes=lista)

# ---------------- EXECUÇÃO ----------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



