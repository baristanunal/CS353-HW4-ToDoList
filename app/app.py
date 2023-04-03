
import re
import os
import datetime

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.secret_key = 'abcdefgh'

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'cs353hw4db'

mysql = MySQL(app)


@app.route('/')

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = % s AND password = % s', (username, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            message = 'Logged in successfully!'
            return redirect(url_for('tasks'))
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html', message = message)


@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            message = 'Choose a different username!'

        elif not username or not password or not email:
            message = 'Please fill out the form!'

        else:
            cursor.execute('INSERT INTO User (id, username, email, password) VALUES (NULL, % s, % s, % s)', (username, email, password,))
            mysql.connection.commit()
            message = 'User successfully created!'

    elif request.method == 'POST':
        message = 'Please fill all the fields!'

    return render_template('register.html', message = message)

@app.route('/tasks', methods =['GET', 'POST'])
def tasks():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT * FROM TodoTask WHERE user_id = % s', (session['userid'],))
    todo_tasks = cursor.fetchall()

    cursor.execute('SELECT * FROM DoneTask WHERE user_id = % s', (session['userid'],))
    done_tasks = cursor.fetchall()

    return render_template('tasks.html', todo_tasks=todo_tasks, done_tasks=done_tasks,)

@app.route('/add_task', methods =['GET', 'POST'])
def add_task():
    message = ''

    if request.method == 'POST' and 'title' in request.form and 'description' in request.form and 'deadline' in request.form and 'task_type' in request.form:
        title = request.form['title']
        description = request.form['description']
        deadline = request.form['deadline']
        creation_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_id = session['userid']
        task_type = request.form['task_type']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if not title or not description or not deadline or not task_type:
            message = 'Please fill out the form!'

        else:
            cursor.execute('INSERT INTO ActiveTask (id, title, description, deadline, creation_time, '
                          'user_id, task_type) VALUES (NULL, % s, % s, % s, % s, % s, % s )',
                          (title, description, deadline, creation_time, user_id, task_type, ))
            mysql.connection.commit()
            message = 'Task successfully created!'

    elif request.method == 'POST':
        message = 'Please fill all the fields!'

    return render_template('addTask.html', message=message)

@app.route('/delete_task', methods =['GET', 'POST'])
def delete_task():
    message = ''

    if request.method == 'POST' and 'del_id' in request.form:
        task_id = request.form['del_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM TodoTask WHERE ( id = % s ) ', task_id)
        mysql.connection.commit()
        message = 'Task successfully deleted!'

    return redirect(url_for('tasks'))


@app.route('/analysis', methods =['GET', 'POST'])
def analysis():
    return "Analysis page"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
