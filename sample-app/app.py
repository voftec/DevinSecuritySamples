from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)

# Intentionally vulnerable sample app for educational purposes only.
# Do not deploy in production.

DATABASE = os.path.join(os.path.dirname(__file__), 'sample.db')


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.before_request
def init_db():
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT
        );
        INSERT OR IGNORE INTO users (id, username, password, role) VALUES
        (1, 'admin', 'password123', 'admin'),
        (2, 'alice', 'alice', 'user');
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return 'Insecure API demo'


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # SQL injection
    conn = get_db()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = conn.execute(query).fetchone()
    conn.close()
    if user:
        return jsonify({'status': 'ok', 'role': user['role']})
    return jsonify({'status': 'fail'}), 401


@app.route('/admin/users/<int:user_id>')
def admin_user(user_id):
    # IDOR: admin endpoint has no authorization check
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user))
    return jsonify({'error': 'not found'}), 404


STATIC_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), 'static'))


@app.route('/files')
def files():
    filename = request.args.get('name', 'notes.txt')
    safe_name = secure_filename(filename)
    if not safe_name:
        return jsonify({'error': 'invalid filename'}), 400
    path = os.path.realpath(os.path.join(STATIC_DIR, safe_name))
    if os.path.commonpath([path, STATIC_DIR]) != STATIC_DIR or not os.path.isfile(path):
        return jsonify({'error': 'not found'}), 404
    return send_file(path)


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
