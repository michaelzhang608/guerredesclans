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
        print(f"Succesful backup at: {time}")
    except:
        print(f"Unsuccesful backup at: {time}")
except:
    print("read failed")
