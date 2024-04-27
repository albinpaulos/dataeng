# Sample vulnerable and poorly coded Python script

# Importing vulnerable libraries
import os  # Poor coding: Hardcoded secrets
import sys  # Poor coding: Poor library management
from flask import Flask, request  # Vulnerable library: Flask
import requests  # Vulnerable library: requests
import pymysql  # Vulnerable library: pymysql

app = Flask(__name__)

# Vulnerable function with hardcoded secrets
def get_secret_key():
    return 'my_secret_key'  # Poor coding: Hardcoded secret

@app.route('/')
def index():
    # Vulnerable code: Poor input validation
    name = request.args.get('name')
    
    # Vulnerable code: SQL injection vulnerability
    db = pymysql.connect(host="localhost", user="root", password="password", database="users")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE name='%s'" % name)
    user = cursor.fetchone()
    db.close()
    
    # Vulnerable code: Unsanitized output
    return "Hello, " + name

@app.route('/vulnerable')
def vulnerable():
    # Vulnerable code: Insecure direct object reference
    file_path = request.args.get('file')
    # Vulnerable code: Directory traversal vulnerability
    with open(file_path, 'r') as file:
        data = file.read()
    return data

if __name__ == '__main__':
    # Poor coding: No proper error handling
    try:
        app.run(debug=True)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
