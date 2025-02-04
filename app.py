from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criar tabela de inscrições
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS inscricoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            curso TEXT NOT NULL,
            horario TEXT NOT NULL,
            local TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar inscrições
@app.route('/inscrever', methods=['POST'])
def inscrever():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        curso = request.form['curso']
        horario = request.form['horario']
        local = request.form['local']

        # Validação básica
        if not nome or not email or not telefone or not curso or not horario or not local:
            flash('Por favor, preencha todos os campos.', 'error')
            return redirect(url_for('index'))

        # Salvar no banco de dados
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO inscricoes (nome, email, telefone, curso, horario, local)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, email, telefone, curso, horario, local))
        conn.commit()
        conn.close()

        flash('Inscrição realizada com sucesso! Aguarde nosso contato.', 'success')
        return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

    from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Função para verificar login
def verificar_login(username, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM usuarios WHERE username = ?', (username,)).fetchone()
    conn.close()
    if user and check_password_hash(user['password'], password):
        return True
    return False

# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verificar_login(username, password):
            session['logged_in'] = True
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Usuário ou senha incorretos.', 'error')
    return render_template('login.html')

# Rota de Logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))

# Rota de Administração (Protegida)
@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    inscricoes = conn.execute('SELECT * FROM inscricoes').fetchall()
    conn.close()
    return render_template('admin.html', inscricoes=inscricoes)

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# Rota para gerar relatório em Excel
@app.route('/exportar-excel')
def exportar_excel():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    df = pd.read_sql_query('SELECT * FROM inscricoes', conn)
    conn.close()
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, download_name='inscricoes.xlsx', as_attachment=True)

# Rota para gerar relatório em PDF
@app.route('/exportar-pdf')
def exportar_pdf():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    inscricoes = conn.execute('SELECT * FROM inscricoes').fetchall()
    conn.close()
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Relatório de Inscrições")
    y = 730
    for inscricao in inscricoes:
        c.drawString(100, y, f"Nome: {inscricao['nome']}, Curso: {inscricao['curso']}, Local: {inscricao['local']}")
        y -= 20
    c.save()
    buffer.seek(0)
    return send_file(buffer, download_name='inscricoes.pdf', as_attachment=True)