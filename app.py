from flask import Flask,render_template,request,session,logging,url_for,redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

# Register form
@app.route("/register")
def register():
    return render_template("register.html")

# Login form
@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)