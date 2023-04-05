
import re
import os
import datetime

from MySQLdb.constants.FIELD_TYPE import NULL
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__, static_url_path='/static', static_folder='static')

app.secret_key = 'abcdefgh'

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'cs353hw4db'

mysql = MySQL(app)

@app.route('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * '
                       'FROM User '
                       'WHERE username = % s AND password = % s', (username, password, ))
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
    return render_template('login.html', message=message)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    message = ''
    if session['loggedin']:
        session['loggedin'] = False
        session['userid'] = NULL
        session['username'] = NULL
        session['email'] = NULL
        message = 'Logged out successfully!'
    else:
        message = 'You have to be logged in to logout.'
    return render_template('login.html', message=message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * '
                       'FROM User '
                       'WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            message = 'Choose a different username!'

        elif not username or not password or not email:
            message = 'Please fill out the form!'

        else:
            cursor.execute('INSERT INTO User (id, username, email, password) '
                           'VALUES (NULL, % s, % s, % s)', (username, email, password,))
            mysql.connection.commit()
            message = 'User successfully created!'

    elif request.method == 'POST':
        message = 'Please fill all the fields!'

    return render_template('register.html', message=message)


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if session['loggedin']:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT id, title, description, deadline, creation_time, task_type '
                       'FROM TodoTask '
                       'WHERE user_id = %s', (session['userid'],))
        todo_tasks = cursor.fetchall()

        cursor.execute('SELECT id, title, description, deadline, creation_time, done_time, task_type '
                       'FROM DoneTask '
                       'WHERE user_id = % s', (session['userid'],))
        done_tasks = cursor.fetchall()

        return render_template('tasks.html', todo_tasks=todo_tasks, done_tasks=done_tasks, )

    else:
        return redirect(url_for('login'))


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    message = ''

    if request.method == 'POST' and 'title' in request.form and 'description' in request.form \
      and 'deadline' in request.form and 'task_type' in request.form:
        title = request.form['title']
        description = request.form['description']
        deadline = request.form['deadline']
        creation_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_id = session['userid']
        task_type = request.form['task_type']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if not title or not description or not deadline or not task_type:
            message = 'Please fill out the form!'
            return render_template('addTask.html', message=message)

        else:
            cursor.execute('INSERT INTO TodoTask (id, title, description, deadline, creation_time, '
                           'user_id, task_type) '
                           'VALUES (NULL, % s, % s, % s, % s, % s, % s )',
                           (title, description, deadline, creation_time, user_id, task_type, ))
            mysql.connection.commit()
            message = 'Task successfully created!'
            return redirect(url_for('tasks'))

    elif request.method == 'POST':
        message = 'Please fill all the fields!'

    return render_template('addTask.html', message=message)


@app.route('/view_edit_task', methods=['GET', 'POST'])
def view_edit_task():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_id = session['userid']
    task_id = request.form['task_id']

    cursor.execute('SELECT * '
                   'FROM TodoTask '
                   'WHERE id = % s', (task_id, ))
    task_to_be_edited = cursor.fetchone()
    title = task_to_be_edited['title']
    description = task_to_be_edited['description']
    deadline = task_to_be_edited['deadline']
    task_type = task_to_be_edited['task_type']

    return render_template('viewEditTask.html', task_id=task_id, title=title, description=description,
                           deadline=deadline, task_type=task_type)


@app.route('/edit_task', methods=['GET', 'POST'])
def edit_task():
    message = ''

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_id = session['userid']
    task_id = request.form['task_id']

    if request.method == 'POST' and 'title' in request.form and 'description' in request.form \
      and 'deadline' in request.form and 'task_type' in request.form:
        title = request.form['title']
        description = request.form['description']
        deadline = request.form['deadline']
        task_type = request.form['task_type']

        if not title or not description or not deadline or not task_type:
            message = 'Please fill out the form!'

        else:
            cursor.execute('UPDATE TodoTask '
                           'SET title = % s, description = % s, deadline = % s, task_type = % s '
                           'WHERE id = % s', (title, description, deadline, task_type, task_id, ))
            mysql.connection.commit()
            message = 'Task successfully edited!'
        return redirect(url_for('tasks'))

    else:
        cursor.execute('SELECT * '
                       'FROM TodoTask '
                       'WHERE id = % s', (task_id, ))
        task_to_be_edited = cursor.fetchone()
        title = task_to_be_edited['title']
        description = task_to_be_edited['description']
        deadline = task_to_be_edited['deadline']
        task_type = task_to_be_edited['task_type']
        message = 'Please fill all the fields!'

        return render_template('viewEditTask.html', task_id=task_id, title=title, description=description,
                               deadline=deadline, task_type=task_type, message=message)


@app.route('/delete_task', methods=['GET', 'POST'])
def delete_task():

    if request.method == 'POST' and 'task_id' in request.form:
        task_id = request.form['task_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM TodoTask '
                       'WHERE (id = % s) ', (task_id, ))
        mysql.connection.commit()
        message = 'Task successfully deleted!'

    return redirect(url_for('tasks'))


@app.route('/finish_task', methods=['GET', 'POST'])
def finish_task():

    task_id = request.form['task_id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT * '
                   'FROM TodoTask '
                   'WHERE id = % s', (task_id, ))
    task_to_be_finished = cursor.fetchone()
    title = task_to_be_finished['title']
    description = task_to_be_finished['description']
    deadline = task_to_be_finished['deadline']
    creation_time = task_to_be_finished['creation_time']
    done_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_id = task_to_be_finished['user_id']
    task_type = task_to_be_finished['task_type']

    cursor.execute('INSERT INTO DoneTask(id, title, description, deadline, '
                   'creation_time, done_time, user_id, task_type)'
                   'VALUES (NULL, % s, % s, % s, % s, % s, % s, % s)',
                   (title, description, deadline, creation_time, done_time, user_id, task_type, ))

    cursor.execute('DELETE FROM TodoTask '
                   'WHERE id = % s', (task_id, ))
    mysql.connection.commit()

    return redirect(url_for('tasks'))


@app.route('/analysis', methods=['GET', 'POST'])
def analysis():

    if session['loggedin']:

        user_id = session['userid']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # 1. List the title and latency of the tasks that were completed after their deadlines (for the user).
        cursor.execute('SELECT title, TIMESTAMPDIFF(HOUR, deadline, done_time) AS "latency (in hours)" '
                       'FROM DoneTask '
                       'WHERE user_id = % s AND (done_time > deadline)', (user_id,))
        overdue_tasks = cursor.fetchall()

        # 2. Give the average task completion time of the user.
        cursor.execute('SELECT AVG(TIMESTAMPDIFF(HOUR, creation_time, done_time)) AS "average completion time" '
                       'FROM DoneTask '
                       'WHERE user_id = % s', (user_id, ))
        avg_comp_time = cursor.fetchone()['average completion time']

        # 3. List the number of the completed tasks per task type, in descending order (for the user).
        cursor.execute('SELECT task_type, COUNT(*) AS "completed tasks" '
                       'FROM DoneTask '
                       'WHERE user_id = % s '
                       'GROUP BY task_type '
                       'ORDER BY "completed tasks" DESC', (user_id, ))
        completed_task_count = cursor.fetchall()

        # 4. List the title and deadline of uncompleted tasks in increasing order of deadlines (for the user).
        cursor.execute('SELECT title, deadline '
                       'FROM TodoTask '
                       'WHERE user_id = % s '
                       'ORDER BY deadline ASC', (user_id, ))
        todo_tasks = cursor.fetchall()

        # 5. List the title and task completion time of the top 2 completed tasks that took the most time, in
        #    descending order (for the user).
        cursor.execute('SELECT title, TIMESTAMPDIFF(HOUR, creation_time, done_time) '
                       'AS "task completion time (in hours)" '
                       'FROM DoneTask '
                       'WHERE user_id = % s '
                       'ORDER BY "task completion time (in hours)" '
                       'LIMIT 2', (user_id, ))
        longest_tasks = cursor.fetchall()

        return render_template('analysis.html', overdue_tasks=overdue_tasks, avg_comp_time=avg_comp_time,
                               completed_task_count=completed_task_count, todo_tasks=todo_tasks,
                               longest_tasks=longest_tasks)

    else:
        return redirect(url_for('login'))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
