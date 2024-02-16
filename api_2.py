import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DATABASE = 'database.db'

# Create database tables
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                user_id INTEGER,
                company_id INTEGER,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(company_id) REFERENCES companies(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        conn.commit()

# Initialize database tables
init_db()

# Endpoint for listing Users
@app.route('/users', methods=['GET'])
def list_users():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
    return jsonify(users)

# Endpoint for creating a new User
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, email) VALUES (?, ?)', (data['username'], data['email']))
        conn.commit()
    return jsonify(data), 201

# Endpoint for listing Clients
@app.route('/clients', methods=['GET'])
def list_clients():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients')
        clients = cursor.fetchall()
    return jsonify(clients)

# Endpoint for creating a new Client
@app.route('/clients', methods=['POST'])
def create_client():
    data = request.json
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO clients (name, user_id, company_id, email, phone) VALUES (?, ?, ?, ?, ?)',
                       (data['name'], data['user_id'], data['company_id'], data['email'], data['phone']))
        conn.commit()
    return jsonify(data), 201

# Endpoint for listing Companies
@app.route('/companies', methods=['GET'])
def list_companies():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM companies')
        companies = cursor.fetchall()
    return jsonify(companies)

# Endpoint for creating a new Company
@app.route('/companies', methods=['POST'])
def create_company():
    data = request.json
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO companies (name) VALUES (?)', (data['name'],))
        conn.commit()
    return jsonify(data), 201

if __name__ == '__main__':
    app.run(debug=True)
