from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_users'
app.config['MYSQL_PORT'] = 3307

mysql = MySQL(app)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT username, password from tbl_users WHERE username = '{username}'")
        user = cur.fetchone()
        cur.close()
        if user and pwd == user[1]:
            session['username'] = user[0]
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO tbl_users (username, password) VALUES ('{username}', '{pwd}')")
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/xss', methods=['GET', 'POST'])
def xss_demo():
    user_input = ''
    if request.method == 'POST':
        # No sanitization
        user_input = request.form.get('user_input', '')
    # Passed to the template
    return render_template('xss.html', user_input=user_input)

@app.route('/get_user_details')
def get_user_details():
    username = 'admin'  #Uses admin for example
    cur = mysql.connection.cursor()
    cur.execute("SELECT username, password FROM tbl_users WHERE username = %s", (username,)) # Fetches details from the flask_user table
    user = cur.fetchone() #Fetches the row of data containing admin
    cur.close()
    if user:
        return jsonify({"username": user[0], "password": user[1]}) #If it contains the user data, it's displayed
    else:
        return jsonify({"error": "User not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
