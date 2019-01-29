from flask import Flask, render_template, request
import os
from utils import check_pass, read_csv, write_csv
import time
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'

@app.route("/")
def index():
    return render_template("index.html", points=get_points())

@app.route("/update_points", methods=["POST"])
def add_points():
    points = request.form.get("points")
    clan = request.form.get("clan")
    password = request.form.get("password")
    result = add_points([clan, points], password)

    return render_template("index.html", points=get_points())

def get_points(clan=None):
    # Get points
    f = read_csv("/static/db.csv")
    m = max([int(i[1]) for i in f])
    # Compute percents
    out = {k: (int(v), round(100 * int(v) / m)) for k, v in f}
    if not clan:
        return [[k, v] for k,v in out.items()]
    else:
        return out[clan]

def add_points(change, password):
    if check_pass("/static/password.txt", password):
        points = [[p[0], p[1][0]] for p in get_points()]
        for p in points:
            if p[0] == change[0]:
                p[1] = p[1] + int(change[1])
        log = read_csv("/home/guerredesclans/mysite/log.csv")
        log.append([datetime.now(), change[0], change[1]])
        write_csv("/static/log.csv", log)
        write_csv("/static/db.csv", points)
        return change[0]
    else:
        return False

if __name__ == "__main__":
    os.environ["FLASK_APP"] = "flask_app.py"
    # LOCAL FILE
    os.system("flask run")
