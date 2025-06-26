from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY, name TEXT, status TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY, filename TEXT, status TEXT)")
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        status = request.form['status']
        cursor.execute("INSERT INTO attendance (name, status) VALUES (?, ?)", (name, status))
        conn.commit()
        return redirect(url_for('attendance'))  # Refresh page after submitting data
    cursor.execute("SELECT * FROM attendance")
    data = cursor.fetchall()
    conn.close()
    return render_template('attendance.html', records=data)

@app.route('/files', methods=['GET', 'POST'])
def files():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    if request.method == 'POST':
        filename = request.form['filename']
        status = request.form['status']
        cursor.execute("INSERT INTO files (filename, status) VALUES (?, ?)", (filename, status))
        conn.commit()
        return redirect(url_for('files'))  # Refresh page after submitting data
    cursor.execute("SELECT * FROM files")
    data = cursor.fetchall()
    conn.close()
    return render_template('files.html', records=data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)