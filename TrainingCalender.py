import argparse
from datetime import datetime
import sqlite3

class Database():
    def __init__(self, database: str):
        self.db = sqlite3.connect(database).cursor()
        self.db.execute("""CREATE TABLE IF NOT EXISTS workouts (
                        id  INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        time INTEGER NOT NULL,
                        "index" INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        intensity INTEGER NOT NULL
                        )""")
    
    def add(self, date, time, index, name, intensity):
        self.db.execute("""INSERT INTO workouts VALUES (?, ?, ?, ?, ?)""", (date, time, index, name, intensity))

def valid_date(date_str: str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date: '{date_str}'. Use YYYY-MM-DD")

def valid_date_range(date_str: str):
    try:
        if date_str.count("/") != 1:
            raise ValueError()
        start_str, end_str = date_str.split("/")
        start_date = datetime.strptime(start_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_str, "%Y-%m-%d")
        if start_date > end_date:
            raise ValueError()
        return date_str
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid range: '{date_str}'. Use YYYY-MM-DD/YYYY-MM-DD")

def add(args, db: Database):
    db.add(args.date, args.time, args.index, args.name, args.intensity)

def view(args, db):
    ...

def edit(args, db):
    ...

def copy(args, db):
    ...

def main():
    parser = argparse.ArgumentParser(prog="TrainingCalender",
                                    description="A CLI tool for managing your training plan.")

    subparser = parser.add_subparsers(dest="command", required=True)

    parser_add = subparser.add_parser("add", help="Add a new workout")
    parser_add.add_argument("-d", "--date", required=True, type=valid_date, help="Date for workout [YYYY-MM-DD]")
    parser_add.add_argument("-i", "--index", default=-1, type=int, help="Day index for workout")
    parser_add.add_argument("-T", "--time", type=int, required=True, help="Time for workout")
    parser_add.add_argument("-n", "--name", type=str, required=True, help="Name of workout")
    parser_add.add_argument("-I", "--intensity", type=int, required=True, help="Intensity of workout")
    parser_add.set_defaults(func=add)

    parser_view= subparser.add_parser("view", help="View a set of workouts")
    parser_view.add_argument("-r", "--range", type=valid_date_range, help="Select range to search in [YYYY-MM-DD/YYYY-MM-DD]")
    parser_view.set_defaults(func=view)

    args = parser.parse_args()

    db = Database("workouts.db")

    args.func(args, db)

if __name__ == "__main__":
    main()