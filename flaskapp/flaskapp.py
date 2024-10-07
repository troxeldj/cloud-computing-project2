from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

DATABASE_PATH = '/home/ubuntu/flaskapp/mydatabase.db'

app = Flask(__name__)

app.secret_key = 'SUPERSECRETSECRET'

logged_in_user = ''

# SQLite setup
conn = sqlite3.connect(DATABASE_PATH)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, firstname TEXT, lastname TEXT, email TEXT);')
conn.commit()  
conn.close()


@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    
    # Add user to database
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, firstname, lastname, email) VALUES (?,?,?,?,?)', (username, password, firstname, lastname, email))
    conn.commit()
    conn.close()

   # redirect to profile page
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()

    if user and (str(user[1]) == password):
        session['username'] = username
        session['password'] = password
        return redirect(url_for('profile', username=username))
    else:
        return redirect(url_for('index'))
        

@app.route('/profile/<username>/')
def profile(username):
    if session.get('username') == username and session.get('password'):
        # Connect to the database and fetch user details
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()

        # Check if the password in session matches the database password
        if user and user[1] == session['password']:
            return render_template('profile.html', user=user)
        else:
            return redirect(url_for('login'))

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
