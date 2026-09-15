"""
Simple CRUD Task Manager
-------------------------
Backend: Flask + SQLite (REST API)
Frontend: templates/index.html (vanilla HTML/JS, served by Flask)

Run with:
    pip install flask
    python app.py

Then open http://127.0.0.1:5000 in your browser.
"""

from flask import Flask, jsonify, request, render_template
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            done INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()


# ---------- Frontend route ----------

@app.route("/")
def index():
    return render_template("index.html")


# ---------- CRUD API routes ----------

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    conn.close()
    tasks = [dict(row) for row in rows]
    return jsonify(tasks)


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(dict(row))


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(force=True) or {}
    title = (data.get("title") or "").strip()
    description = (data.get("description") or "").strip()

    if not title:
        return jsonify({"error": "Title is required"}), 400

    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO tasks (title, description, done) VALUES (?, ?, 0)",
        (title, description),
    )
    conn.commit()
    new_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (new_id,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(force=True) or {}

    conn = get_db()
    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if existing is None:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    title = data.get("title", existing["title"])
    description = data.get("description", existing["description"])
    done = data.get("done", existing["done"])
    done = 1 if done in (1, True, "1", "true", "True") else 0

    conn.execute(
        "UPDATE tasks SET title = ?, description = ?, done = ? WHERE id = ?",
        (title, description, done, task_id),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return jsonify(dict(row))


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if existing is None:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task deleted"}), 200


# Initialize the database on import so it works both with `python app.py`
# (Flask dev server) and with a production server like Gunicorn, which
# imports this module rather than running it as __main__.
init_db()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
