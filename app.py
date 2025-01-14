from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

#Initialize the database
def init_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT NOT NULL, date TEXT NOT NULL, completed INTEGER DEFAULT 0)''') #0 = not completed, 1 = completed
    conn.commit()
    conn.close()

#Add a task
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    date = request.form['date']
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (task, date) VALUES (?, ?)', (task, date))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

#Display all tasks
@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks ORDER BY date')
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

#Delete a task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

#Edit a task
@app.route('/edit/<int:task_id>', methods=['Get', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        task = request.form['task']
        date = request.form['date']
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('UPDATE tasks SET task = ?, date = ? WHERE id = ?', (task, date, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = c.fetchone()
        conn.close()
    return render_template('edit.html', task=task)

#Mark a task as completed
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)