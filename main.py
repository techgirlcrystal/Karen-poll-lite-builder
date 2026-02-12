import os
import psycopg2
from flask import Flask, render_template, jsonify, request
from replit import db

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_conn():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            state VARCHAR(50) NOT NULL,
            vote VARCHAR(10) NOT NULL,
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


init_db()

if "yes" not in db:
    db["yes"] = 0
if "no" not in db:
    db["no"] = 0
if "not_sure" not in db:
    db["not_sure"] = 0


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/vote", methods=["POST"])
def vote():
    choice = request.json.get("choice")
    if choice in ("yes", "no", "not_sure"):
        db[choice] = db[choice] + 1
    return jsonify(get_results())


@app.route("/results")
def results():
    return jsonify(get_results())


@app.route("/comment", methods=["POST"])
def add_comment():
    data = request.json
    first_name = data.get("first_name", "").strip()[:50]
    state = data.get("state", "").strip()[:50]
    comment = data.get("comment", "").strip()[:500]
    vote_choice = data.get("vote", "").strip()

    if not first_name or not state or not comment:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO comments (first_name, state, vote, comment) VALUES (%s, %s, %s, %s)",
        (first_name, state, vote_choice, comment),
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"success": True})


@app.route("/comments")
def get_comments():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT first_name, state, vote, comment, created_at FROM comments ORDER BY created_at DESC LIMIT 50"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    comments = []
    for row in rows:
        label = "Yes" if row[2] == "yes" else ("No" if row[2] == "no" else "Not Sure")
        comments.append({
            "first_name": row[0],
            "state": row[1],
            "vote": label,
            "comment": row[3],
            "time": row[4].strftime("%b %d, %I:%M %p"),
        })
    return jsonify(comments)


def get_results():
    yes = int(db.get("yes", 0))
    no = int(db.get("no", 0))
    not_sure = int(db.get("not_sure", 0))
    total = yes + no + not_sure
    if total == 0:
        return {"yes": 0, "no": 0, "not_sure": 0, "total": 0}
    return {
        "yes": round(yes / total * 100, 1),
        "no": round(no / total * 100, 1),
        "not_sure": round(not_sure / total * 100, 1),
        "total": total,
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
