from flask import Flask, request, jsonify, send_file, session, abort
import sqlite3
import os
import functools

app = Flask(__name__)
# Required for session-based auth and admin checks.
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-not-for-production')

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


def require_login(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'status': 'fail', 'error': 'authentication required'}), 401
        return func(*args, **kwargs)
    return wrapper


def require_admin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('role') != 'admin':
            return jsonify({'status': 'fail', 'error': 'admin required'}), 403
        return func(*args, **kwargs)
    return wrapper


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    # Use a parameterized query to prevent SQL injection.
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ?',
        (username,)
    ).fetchone()
    conn.close()
    if user and user['password'] == password:
        session['user_id'] = user['id']
        session['role'] = user['role']
        return jsonify({'status': 'ok', 'role': user['role']})
    return jsonify({'status': 'fail'}), 401


@app.route('/admin/users/<int:user_id>')
@require_login
@require_admin
def admin_user(user_id):
    # Admin-only endpoint: do not return the password column.
    conn = get_db()
    user = conn.execute(
        'SELECT id, username, role FROM users WHERE id = ?',
        (user_id,)
    ).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user))
    return jsonify({'error': 'not found'}), 404


@app.route('/files')
def files():
    filename = request.args.get('name', 'notes.txt')
    # Prevent path traversal by confining requested files to the static directory.
    base_dir = os.path.dirname(__file__)
    static_dir = os.path.realpath(os.path.join(base_dir, 'static'))
    requested_path = os.path.realpath(os.path.join(static_dir, filename))
    if not requested_path.startswith(static_dir + os.sep):
        return jsonify({'error': 'invalid path'}), 400
    return send_file(requested_path)


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    # Debug mode and 0.0.0.0 are unsafe for anything but local dev.
    # Use a production WSGI server (e.g. gunicorn) for real deployments.
    debug = os.environ.get('FLASK_DEBUG', '0').lower() in ('1', 'true', 'yes')
    app.run(debug=debug, host='127.0.0.1', port=5000)
