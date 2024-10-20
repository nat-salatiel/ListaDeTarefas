from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Dados de configuração para a conexão com o banco de dados MySQL
app.config['MYSQL_HOST'] = 'localhost'  # Endereço do servidor MySQL
app.config['MYSQL_USER'] = 'root'       # Nome de usuário do MySQL
app.config['MYSQL_PASSWORD'] = ''       # Senha do usuário do MySQL (vazia neste caso)
app.config['MYSQL_DB'] = 'aplicativopythonflask'  # Nome do banco de dados a ser utilizado

# Cria uma conexão com o MySQL usando as configurações acima
mysql = MySQL(app)

# Rota principal da aplicação
@app.route('/')
def home():
    cur = mysql.connection.cursor()  # Cria um cursor para executar comandos SQL
    # Executa uma consulta para selecionar tarefas que não estão marcadas como 'del'
    cur.execute("SELECT *, DATE_FORMAT(task_date,'%d/%m/%Y às %H:%i') AS datebr FROM tasks WHERE task_status != 'del'")
    tasks = cur.fetchall()  # Obtém todos os resultados da consulta
    # print('\n\n', tasks, '\n\n')  # Para depuração: imprime as tarefas no console
    cur.close()  # Fecha o cursor
    return render_template('.home.html', tasks=tasks)  # Renderiza o template com as tarefas

# Rota para adicionar uma nova tarefa
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':  # Verifica se o método da requisição é POST
        titulo = request.form['titulo']  # Obtém o título da tarefa do formulário
        descricao = request.form['descricao']  # Obtém a descrição da tarefa do formulário
        cur = mysql.connection.cursor()  # Cria um cursor
        # Executa uma inserção no banco de dados
        cur.execute(
            "INSERT INTO tasks (task_titulo, task_descricao) VALUES (%s, %s)", (titulo, descricao))
        mysql.connection.commit()  # Confirma a transação
        cur.close()  # Fecha o cursor
        return redirect(url_for('home'))  # Redireciona para a página inicial
    return render_template('add_task.html')  # Renderiza o template para adicionar uma tarefa

# Rota para editar uma tarefa existente
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    cur = mysql.connection.cursor()  # Cria um cursor
    if request.method == 'POST':  # Verifica se o método da requisição é POST
        titulo = request.form['titulo']  # Obtém o título do formulário
        descricao = request.form['descricao']  # Obtém a descrição do formulário
        # Verifica se o checkbox de status está marcado
        if request.form.get('status') == 'on':
            status = 'concluído'  # Define como 'concluído' se marcado
        else:
            status = 'pendente'  # Define como 'pendente' se não

        # print('\n\n\n', status, '\n\n\n')  # Para depuração: imprime o status no console

        # Executa uma atualização na tarefa especificada pelo ID
        cur.execute("UPDATE tasks SET task_titulo=%s, task_descricao=%s, task_status=%s WHERE task_id=%s",
                    (titulo, descricao, status, id,))
        mysql.connection.commit()  # Confirma a transação
        cur.close()  # Fecha o cursor
        return redirect(url_for('home'))  # Redireciona para a página inicial
    # Se não for uma requisição POST, busca a tarefa para editar
    cur.execute("SELECT * FROM tasks WHERE task_id=%s", (id,))
    task = cur.fetchone()  # Obtém a tarefa específica

    # print("\n\n", task, "\n\n")  # Para depuração: imprime a tarefa no console

    # Verifica se a tarefa está marcada como 'concluído' para o checkbox
    if task[4] == 'concluido':
        checked = 'checked'  # Marca o checkbox como selecionado
    else:
        checked = ''  # Não marca o checkbox

    cur.close()  # Fecha o cursor
    return render_template('edit_task.html', task=task, checked=checked)  # Renderiza o template de edição

# Rota para deletar uma tarefa
@app.route('/delete/<int:id>')
def delete_task(id):
    cur = mysql.connection.cursor()  # Cria um cursor
    # Executa uma atualização para marcar a tarefa como 'del'
    cur.execute("UPDATE tasks SET task_status = 'del' WHERE task_id=%s", (id,))
    mysql.connection.commit()  # Confirma a transação
    cur.close()  # Fecha o cursor
    return redirect(url_for('home'))  # Redireciona para a página inicial

# Verifica se o script está sendo executado diretamente
if __name__ == '__main__':
    # Inicia o servidor Flask em modo debug
    app.run(debug=True)
