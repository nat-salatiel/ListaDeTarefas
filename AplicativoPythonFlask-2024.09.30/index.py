from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL


# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Dados de conexão
app.config['MYSQL_HOST'] = 'localhost'  # Endereço do servidor MySQL
app.config['MYSQL_USER'] = 'root'       # Nome de usuário do MySQL
app.config['MYSQL_PASSWORD'] = ''       # Senha do usuário do MySQL
app.config['MYSQL_DB'] = 'aplicativopythonflask'  # Nome do banco de dados

# Conecta o Python ao MySQL → `mysql` é a conexão com o banco de dados
mysql = MySQL(app)


@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT *, DATE_FORMAT(task_date,'%d/%m/%Y às %H:%i') AS datebr FROM tasks WHERE task_status != 'del'")
    tasks = cur.fetchall()
    # print('\n\n', tasks, '\n\n')t5hy5hy5h5y
    cur.close()
    return render_template('home.html', tasks=tasks, status='46764 ')


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO tasks (task_titulo, task_descricao) VALUES (%s, %s)", (titulo, descricao))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home'))
    return render_template('add_task.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        status = request.form.get('status', 'off')

        print('\n\n', status, '\n\n')
        # if status != 'on':
        #     status = 'off'

        # print('\n\n', status, '\n\n')
        cur.execute("UPDATE tasks SET task_titulo=%s, task_descricao=%s, task_status=%s WHERE task_id=%s",
                    (titulo, descricao, status, id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home'))
    cur.execute("SELECT * FROM tasks WHERE task_id=%s", (id,))
    task = cur.fetchone()

    print("\n\n", task, "\n\n")

    if task[4] == 'on':
        checked = 'checked'
    else:
        checked = ''

    cur.close()
    return render_template('edit_task.html', task=task, checked=checked)


@app.route('/delete/<int:id>')
def delete_task(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks SET task_status = 'del' WHERE task_id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('home'))


# Verifica se o script está sendo executado diretamente
if __name__ == '__main__':
    # Inicia o servidor Flask em modo debug
    app.run(debug=True)
