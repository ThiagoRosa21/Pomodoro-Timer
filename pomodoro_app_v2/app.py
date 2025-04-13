from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("pomodoro.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_type TEXT,
                duration INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save-session", methods=["POST"])
def save_session():
    data = request.get_json()
    with sqlite3.connect("pomodoro.db") as conn:
        conn.execute("INSERT INTO sessions (session_type, duration) VALUES (?, ?)", 
                     (data["type"], data["duration"]))
    return jsonify({"status": "success"})

@app.route("/dashboard")
def dashboard():
    with sqlite3.connect("pomodoro.db") as conn:
        cursor = conn.execute("""
            SELECT DATE(timestamp), session_type, SUM(duration) 
            FROM sessions 
            GROUP BY DATE(timestamp), session_type
        """)
        stats = cursor.fetchall()
    return render_template("dashboard.html", stats=stats)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)