from flask import Flask, render_template, request, redirect, url_for
from utils import check_pass, read_csv, write_csv, read_file
from collections import Counter
from datetime import datetime
from random import random
from math import log
import subprocess
import time
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'

@app.route("/")
def index():
    return render_template("index.html", data=get_data(), teams=get_teams())

@app.route("/update_points", methods=["GET", "POST"])
def add_points():
    if request.method == "POST":
        points = request.form.get("points")
        clan = request.form.get("clan")
        password = request.form.get("password")
        add_points_clan([clan, points], password)

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route("/add_points_team", methods=["GET", "POST"])
def add_points_team():
    if request.method == "POST":
        team_id = request.form.get("team_id")

        if is_production():
            filename = "/home/guerredesclans/mysite/teams_points"

        else:
            filename = "teams_points"

        with open(filename, "ab") as f:
            f.write(f"{team_id};".encode('utf-8'))
            f.write(f"{team_id};".encode('utf-8'))
            f.write(f"{team_id};".encode('utf-8'))

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

def get_teams():
    if is_production():
        teams = read_csv('/home/guerredesclans/mysite/teams.csv')
        teams_points = read_file('/home/guerredesclans/mysite/teams_points')
    else:
        teams = read_csv('teams.csv')
        teams_points = read_file('teams_points')

    s = ""
    for l in teams_points:
        s += l

    c = Counter(s.split(";"))

    for t in teams:
        team_id = t[4]
        t.insert(4, c[team_id])
    try:
        teams.sort(key=lambda x:int(x[3]), reverse=True)
    except:
        print("Int error")

    return teams

def get_data():
    return json.dumps({
        "clan_points": get_clan_points(),
    })

def safe_log(n, b):
    if n == 0:
        return 0
    else:
        return int(log(n, b))

def get_clan_points():
    # Get points
    if is_production():
        points = read_csv('/home/guerredesclans/mysite/db.csv')
    else:
        points = read_csv('db.csv')

    return points

def add_points_clan(change, password):

    pass_location = 'password.txt'
    log_location = 'log.csv'
    db_location = 'db.csv'

    if is_production():
        pass_location = '/home/guerredesclans/mysite/password.txt'
        log_location = '/home/guerredesclans/mysite/log.csv'
        db_location = '/home/guerredesclans/mysite/db.csv'

    if check_pass(pass_location, password):
        points = get_points()
        for p in points:
            if p[0] == change[0]:
                print(type(p[1]))
                print(type(change[1]))

                p[1] = int(p[1]) + int(change[1])

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
    try:
        current = subprocess.check_output(["lsof", "-t", "-i:5000"])
        current = max(current.decode("utf-8").split("\n"))
        print(f"kill {current}")
        os.system(f"kill {current}")
    except Exception as e:
        print(e)
    os.system("flask run")
