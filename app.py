from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'flash message'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2240'
app.config['MYSQL_DB'] = 'studentsInfo'
app.config['MYSQL_PORT'] = 3307

mysql = MySQL(app)


@app.route('/')
def index():
    try:
        mysql.connection.ping()
        print("Database connection established successfully.")
    except Exception as e:
        print("Error connecting to the database:", str(e))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM studentsinfo.students")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', students=data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        flash('New Student Added')
        name = request.form['s_name']
        address = request.form['s_address']
        phone = request.form['s_phone']
        email = request.form['s_email']
        age = request.form['s_age']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (s_name, s_address, s_phone, s_email, s_age) VALUES (%s, %s, %s, %s, %s)",
                    (name, address, phone, email, age))
        mysql.connection.commit()
        return redirect(url_for('index'))


@app.route('/update/<int:s_id>', methods=['GET', 'POST'])
def update(s_id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['s_name']
        address = request.form['s_address']
        phone = request.form['s_phone']
        email = request.form['s_email']
        age = request.form['s_age']

        cur.execute(
            "UPDATE students SET s_name = %s, s_address = %s, s_phone = %s, s_email = %s, s_age = %s WHERE s_id = %s",
            (name, address, phone, email, age, s_id))
        mysql.connection.commit()
        flash('Student information updated')
        return redirect(url_for('index'))

    cur.execute("SELECT * FROM students WHERE s_id = %s", (s_id,))
    student_data = cur.fetchone()
    cur.close()

    if student_data:
        return render_template('updateInfo.html', row=student_data)
    else:
        flash('Student not found')
        return redirect(url_for('index'))


@app.route('/addInfo.html')
def add_info():
    return render_template('addInfo.html')


@app.route('/delete/<int:id_data>', methods=['GET', 'POST'])
def delete(id_data):
    flash('Data deleted successfully.')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE s_id = %s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
