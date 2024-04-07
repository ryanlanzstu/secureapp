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
        cur.execute("SELECT username, password from tbl_users WHERE username = %s", (username,)) #Add parameterized queries instead
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
        pwd = request.form['password'] #Sensitive Data Exposure
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


#Reflective XSS
@app.route('/xss', methods=['GET', 'POST'])
def xss_demo():
    user_input = ''
    if request.method == 'POST':
        #No sanitization
        user_input = request.form.get('user_input', '')
    #Passed to the template
    return render_template('xss.html', user_input=user_input)

#Reflective XSS
@app.route('/get_user_details')
def get_user_details():
    username = 'admin'  #Uses admin for example
    cur = mysql.connection.cursor()
    cur.execute("SELECT username, password FROM tbl_users WHERE username = %s", (username,)) #Fetches details from the flask_user table
    user = cur.fetchone() #Fetches the row of data containing admin
    cur.close()
    if user:
        return jsonify({"username": user[0], "password": user[1]}) #If it contains the user data, it's displayed
    else:
        return jsonify({"error": "User not found"}), 404
    
@app.route('/xss/dom')
def dom_xss_demo():
    return render_template('xss_dom.html')


@app.route('/log_xss', methods=['POST'])
def log_xss():
    user_input = request.form.get('user_input', '')
    username = session.get('username', None)

    if username and user_input:
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tbl_xss (username, xss_text) VALUES (%s, %s)", (username, user_input))
            mysql.connection.commit()
            print("XSS submission logged successfully.")
        except Exception as e:
            print(f"Error logging XSS submission: {e}")
        finally:
            cur.close()
    else:
        print("No username in session or empty user input.")

    return '', 204  #Kept on loggin the attack but then not displaying the attack


@app.route('/xss_logs')
def xss_logs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_xss ORDER BY time DESC") 
    logs = cur.fetchall()
    cur.close()
    return render_template('xss_logs.html', logs=logs)

#https://stackoverflow.com/questions/63290047/flask-csp-content-security-policy-best-practice-against-attack-such-as-cross
@app.after_request
def add_security_headers(resp):
    resp.headers['Content-Security-Policy']='default-src \'self\''
    return resp


if __name__ == '__main__':
    app.run(debug=True)
