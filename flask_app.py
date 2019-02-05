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

@app.route("/update_points", methods=["GET", "POST"])
def add_points():
    if request.method == "POST":
        points = request.form.get("points")
        clan = request.form.get("clan")
        password = request.form.get("password")
        result = add_points([clan, points], password)

        return render_template("index.html", points=get_points())
    else:
        return render_template("index.html", points=get_points())

def get_points(clan=None):
    # Get points
    if is_production():
        f = read_csv('/home/guerredesclans/mysite/db.csv')
    else:
        f = read_csv('db.csv')

    # Compute percents
    m = max([int(i[1]) for i in f])
    out = {k: (int(v), round(100 * int(v) / m)) for k, v in f}
    if not clan:
        return [[k, v] for k,v in out.items()]
    else:
        return out[clan]

def add_points(change, password):

    pass_location = 'password.txt'
    log_location = 'log.csv'
    db_location = 'db.csv'

    if is_production():
        pass_location = '/home/guerredesclans/mysite/password.txt'
        log_location = '/home/guerredesclans/mysite/log.csv'
        db_location = '/home/guerredesclans/mysite/db.csv'

    if check_pass(pass_location, password):
        points = [[p[0], p[1][0]] for p in get_points()]
        for p in points:
            if p[0] == change[0]:
                p[1] = p[1] + int(change[1])

        # Log update
        log = read_csv(log_location)
        log.append([datetime.now(), change[0], change[1]])

        write_csv(log_location, log)
        write_csv(db_location, points)
        return change[0]
    else:
        return False

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

def is_production():
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url != developer_url


if __name__ == "__main__":
    os.environ["FLASK_APP"] = "flask_app.py"
    os.system("flask run")
