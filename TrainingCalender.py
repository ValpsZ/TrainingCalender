import argparse
import datetime
import sqlite3

class Database():
    def __init__(self, database: str):
        self.db = sqlite3.connect(database).cursor()
        self.db.execute("""CREATE TABLE IN NOT EXISTS workouts (
                        id  INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        time INTEGER NOT NULL,
                        index INTERGER NOT NULL,
                        name TEXT NOT NULL,
                        intensity INTEGER NOT NULL,
                        )""")
    
    def add(self, date, time, index, name, intensity):
        self.db.execute("""INSERT INTO workouts VALUES (?, ?, ?, ?, ?)""", (date, time, index, name, intensity))

db = None

def add(args):
    if db == None:
        return

    db.add(args.date, args.time, args.index, args.name, args.intensity)

def view(args):
    ...

def edit(args):
    ...

def copy(args):
    ...

def main():
    global db
    db = Database("workouts.db")

    parser = argparse.ArgumentParser(prog="TrainingCalender",
                                    description="A CLI tool for managing your training plan.")

    subparser = parser.add_subparsers(dest="command", required=True)

    parser_add = subparser.add_parser("add", help="Add a new workout")
    parser_add.add_argument("-d", "--date", required=True, type=str, help="Date for workout [yyyy-mm-dd]")
    parser_add.add_argument("-i", "--index", default=-1, type=int, help="Day index for workout")
    parser_add.add_argument("-t", "--time", type=int, required=True, help="Time for workout")
    parser_add.add_argument("-n", "--name", type=str, required=True, help="Name of workout")
    parser_add.add_argument("-in --intensity", type=int, required=True, help="Intensity of workout")
    parser_add.set_defaults(func=add)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()