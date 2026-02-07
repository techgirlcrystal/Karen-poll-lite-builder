from flask import Flask, render_template, jsonify, request
from replit import db

app = Flask(__name__)

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
