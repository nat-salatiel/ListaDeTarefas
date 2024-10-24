from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from datetime import datetime

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Configurações do banco de dados MySQL
app.config['MYSQL_HOST'] = 'localhost'  # Endereço do servidor MySQL
app.config['MYSQL_USER'] = 'root'       # Nome de usuário do MySQL
app.config['MYSQL_PASSWORD'] = ''       # Senha do usuário do MySQL (vazia neste caso)
app.config['MYSQL_DB'] = 'aplicativopythonflask'  # Nome do banco de dados a ser utilizado

# Inicializa a conexão com o MySQL
mysql = MySQL(app)

def get_cursor():
    """Cria e retorna um cursor para executar comandos SQL no banco de dados."""
    return mysql.connection.cursor()

@app.route('/')
def home():
    """Rota principal que exibe as tarefas não deletadas."""
    cur = get_cursor()
    # Consulta para selecionar tarefas que não estão marcadas como 'del'
    cur.execute("""
        SELECT *, DATE_FORMAT(task_date, '%d/%m/%Y às %H:%i') AS datebr 
        FROM tasks 
        WHERE task_status != 'del' 
        ORDER BY task_status='concluido'
    """)
    tasks = cur.fetchall()  # Obtém todos os resultados da consulta
    cur.close()  # Fecha o cursor
    return render_template('.home.html', tasks=tasks)  # Renderiza o template com as tarefas

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    """Rota para adicionar uma nova tarefa."""
    if request.method == 'POST':  # Verifica se o método da requisição é POST
        title = request.form['title']  # Obtém o título da tarefa do formulário
        description = request.form['description']  # Obtém a descrição da tarefa do formulário
        cur = get_cursor()  # Cria um cursor
        # Insere a nova tarefa no banco de dados
        cur.execute("INSERT INTO tasks (task_title, task_description) VALUES (%s, %s)", (title, description))
        mysql.connection.commit()  # Confirma a transação
        cur.close()  # Fecha o cursor
        return redirect(url_for('home'))  # Redireciona para a página inicial
    return render_template('add_task.html')  # Renderiza o template para adicionar uma tarefa

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    """Rota para editar uma tarefa existente."""
    cur = get_cursor()  # Cria um cursor
    if request.method == 'POST':  # Verifica se o método da requisição é POST
        title = request.form['title']  # Obtém o título da tarefa do formulário
        description = request.form['description']  # Obtém a descrição da tarefa do formulário
        status = 'concluído' if request.form.get('status') == 'on' else 'pendente'  # Define o status da tarefa
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Obtém a data e hora atuais

        # Atualiza a tarefa no banco de dados
        cur.execute("""
            UPDATE tasks 
            SET task_title=%s, task_description=%s, task_date=%s, task_status=%s 
            WHERE task_id=%s
        """, (title, description, current_datetime, status, id))
        mysql.connection.commit()  # Confirma a transação
        cur.close()  # Fecha o cursor
        return redirect(url_for('home'))  # Redireciona para a página inicial

    # Obtém os dados da tarefa a ser editada
    cur.execute("SELECT * FROM tasks WHERE task_id=%s", (id,))
    task = cur.fetchone()  # Obtém a tarefa
    checked = 'checked' if task[4] == 'concluido' else ''  # Marca como concluída se aplicável
    cur.close()  # Fecha o cursor
    return render_template('edit_task.html', task=task, checked=checked)  # Renderiza o template de edição

@app.route('/delete/<int:id>')
def delete_task(id):
    """Rota para deletar uma tarefa, marcando-a como 'del'."""
    cur = get_cursor()  # Cria um cursor
    cur.execute("UPDATE tasks SET task_status = 'del' WHERE task_id=%s", (id,))  # Marca a tarefa como deletada
    mysql.connection.commit()  # Confirma a transação
    cur.close()  # Fecha o cursor
    return redirect(url_for('home'))  # Redireciona para a página inicial

@app.errorhandler(404)
def page_not_found(e):
    """Rota para tratar erros 404 (página não encontrada)."""
    return render_template('404.html'), 404  # Renderiza uma página de erro 404

if __name__ == '__main__':
    app.run(debug=True)  # Inicia a aplicação em modo de depuração
