from datetime import datetime
import csv

from utils import read_csv

try:
    teams = read_csv("teams.csv")
    try:
        time = datetime.now().strftime("%Y-%m-%d %H:%m:%S")
        with open("backup_db/" + time + ".csv", "a") as f:
            w = csv.writer(f)
            for line in teams:
                w.writerow(line)
        print("Succesful backup at:", time)
    except:
        print("Unsuccesful backup at:", time)
except:
    print("read attempt 1 failed")
    try:
        teams = read_csv("/home/guerredesclans/teams.csv")
        try:
            time = datetime.now().strftime("%Y-%m-%d %H:%m:%S")
            with open("/home/guerredesclans/backup_db/" + time + ".csv", "a") as f:
                w = csv.writer(f)
                for line in teams:
                    w.writerow(line)
            print("Succesful backup at:", time)
        except:
            print("Unsuccesful backup at:", time)
    except:
        print("read attemp 2 failed")
