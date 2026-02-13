from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Secret Key from environment
app.secret_key = os.environ.get("SECRET_KEY", "devkey")

# Database Path (Render persistent disk support)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "12345")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            mode TEXT,
            location TEXT,
            budget INTEGER,
            area INTEGER,
            owner_name TEXT,
            owner_contact TEXT,
            status TEXT,
            created_at TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT,
            requirement TEXT,
            property_type TEXT,
            location TEXT,
            budget INTEGER,
            followup_date TEXT,
            status TEXT,
            created_at TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

@app.route("/")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/login")

    conn = get_db_connection()
    properties = conn.execute("SELECT COUNT(*) as count FROM properties").fetchone()
    clients = conn.execute("SELECT COUNT(*) as count FROM clients").fetchone()
    conn.close()

    return render_template("dashboard.html",
                           property_count=properties["count"],
                           client_count=clients["count"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/health")
def health():
    return {"status": "alive"}

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)