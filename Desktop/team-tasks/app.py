from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from datetime import datetime
import os

app = Flask(__name__)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

# Initialize MySQL
mysql = MySQL(app)

def init_db():
    try:
        conn = mysql.connection
        cur = conn.cursor()
        # Create tasks table if it doesn't exist
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                project VARCHAR(255),
                start_time DATETIME,
                end_time DATETIME,
                status VARCHAR(50) DEFAULT 'Pending'
            )
        ''')
        conn.commit()
        cur.close()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")

@app.route('/')
def home():
    try:
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks")
        tasks = cur.fetchall()
        cur.close()
        return render_template("home.html", tasks=tasks)
    except Exception as e:
        return f"Error loading tasks: {str(e)}"

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            project = request.form['project']
            start_time = request.form['start_time']
            end_time = request.form['end_time']

            # Validate input
            if not title or not start_time or not end_time:
                return "Error: Title, Start Time, and End Time are required."

            # Add the task to the database
            cur = mysql.connection.cursor()
            cur.execute('''
                INSERT INTO tasks (title, description, project, start_time, end_time)
                VALUES (%s, %s, %s, %s, %s)
            ''', (title, description, project, start_time, end_time))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('home'))
        except Exception as e:
            return f"Error adding task: {str(e)}"

    return render_template("add_task.html")

@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    try:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            status = request.form['status']
            cur.execute("UPDATE tasks SET status = %s WHERE id = %s", (status, task_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('home'))

        cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cur.fetchone()
        cur.close()
        return render_template("update_task.html", task=task)
    except Exception as e:
        return f"Error updating task: {str(e)}"

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error deleting task: {str(e)}"

if __name__ == '__main__':
    with app.app_context():
        init_db()  # Initialize the database
    app.run(host='0.0.0.0', port=5000, debug=True)
