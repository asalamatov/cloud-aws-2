from flask import Flask, render_template, request, redirect, url_for
from collections import Counter
import csv
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath('/home/ubuntu/flaskapp/'))
DB_PATH = os.path.join(BASE_DIR, "users.db")


def initialize_db():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE if not exists users(username TEXT, password TEXT, firstname TEXT, lastname TEXT, email TEXT)""")
    conn.commit()
    conn.close()

@app.route('/')
def hello_world():
  return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, firstname, lastname, email) VALUES (?, ?, ?, ?, ?)",
              (username, password, firstname, lastname, email))
    conn.commit()
    conn.close()

    return redirect(url_for('profile', username=username))

@app.route('/profile/<username>')
def profile(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.commit()
    conn.close()

    return render_template('profile.html', user=user)

if __name__ == '__main__':
    initialize_db()
    app.run()
