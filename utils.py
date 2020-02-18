import csv
import hashlib

def check_pass(solution_dir, attempt):

    # Get hashed password
    with open(solution_dir, "r") as f:
        for l in f:
            hex_pass_true = l

    # Hash input password and check if match
    hex_pass = hashlib.sha256(attempt.encode()).hexdigest()
    if hex_pass == hex_pass_true:
        return True

    return False

def read_csv(filename):
        out = []
        with open(filename, "r") as f:
            r = csv.reader(f)
            for l in r:
                out.append(l)
        return out

def write_csv(filename, content):
    with open(filename, "w") as f:
        w = csv.writer(f)
        for l in content:
            w.writerow(l)
    return read_csv(filename)

def clear_csv(filename):
    with open(filename, "r+") as f:
        f.truncate(0)

def read_file(filename):
    out = []
    with open(filename, "r") as f:
        for line in f:
            out.append(line)
    return out

def get_input(prompt, is_int=False, int_range=None):
    while True:
        out = input(prompt)
        if out:
            if is_int:
                try:
                    out = int(out)
                except ValueError:
                    continue
                if int_range:
                    if int_range[0] > out or out > int_range[1]:
                        continue
            return out
