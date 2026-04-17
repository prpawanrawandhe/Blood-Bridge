import mysql.connector
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="blood_bridge"
)

cursor = db.cursor(buffered=True)

@app.route('/')
def homepage():
    name = None

    if 'user' in session:
        email = session['user']
        cursor.execute("SELECT name FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        if user:
            name = user[0]

    return render_template('homepage.html', name=name)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        blood_group = request.form['blood_group']
        city = request.form['city']

        cursor.execute(
            "INSERT INTO users (name, email, password, role, blood_group,city) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, email, password, role, blood_group,city)
        )
        db.commit()

        return redirect('/')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('user', None)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            session['user'] = email
            print("u r logged in")
            return redirect('/')
        else:
            return render_template('login.html', error="Invalid Credentials ❌")

    return render_template('login.html')


@app.route('/request', methods=['GET', 'POST'])
def request_blood():
    # print(session)
    if 'user' not in session:
        print("u r not login")
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        blood = request.form['blood_group']
        city = request.form['city']

        cursor.execute(
            "INSERT INTO requests (name, blood_group, city) VALUES (%s,%s,%s)",
            (name, blood, city)
        )
        db.commit()

        cursor.execute(
            "SELECT name, email, blood_group, city FROM users WHERE role='donor' AND blood_group=%s",
            (blood,)
        )
        donors = cursor.fetchall()

        return render_template('result.html', donors=donors)

    return render_template('request.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/donors')
def all_donors():
    cursor.execute("SELECT name, email, blood_group, city FROM users WHERE role='donor'")
    donors = cursor.fetchall()
    return render_template('donors.html', donors=donors)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/nav')
def nav():
    return render_template('nearby.html')


if __name__ == '__main__':
    app.run(debug=True)