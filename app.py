from flask import Flask, render_template, request, redirect, session
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "devkey")

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id SERIAL PRIMARY KEY,
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
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            name TEXT,
            contact TEXT,
            requirement TEXT,
            property_type TEXT,
            location TEXT,
            budget INTEGER,
            followup_date DATE,
            status TEXT,
            created_at TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "12345")

@app.route("/")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM properties")
    property_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM clients")
    client_count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template("dashboard.html",
                           property_count=property_count,
                           client_count=client_count)

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

# Initialize DB when app starts
init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)