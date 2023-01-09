import subprocess
import click
import os
import sqlite3

DB_NAME = "loaders.db"

class InfoDB:
    def __init__(self):
        cpath = os.getcwd()
        if not os.path.isdir(f"{cpath}/.git"):
            print("No git in current dir")
            exit()
        if not os.path.isdir(f"{cpath}/.git/agit"):
            os.mkdir(f"{cpath}/.git/agit")
        db_path = f"{cpath}/.git/agit/{DB_NAME}"
        self.connection: sqlite3.Connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='loaders' ''')
        if (self.cursor.fetchone()[0] == 0):
            self.cursor.execute("CREATE TABLE loaders(load TEXT NOT NULL)")
            self.connection.commit()
    
    def add(self, exec):
        self.cursor.execute("INSERT INTO loaders VALUES (?)", (exec,))
        self.connection.commit()

    def get(self):
        self.cursor.execute("SELECT load FROM loaders")
        return self.cursor.fetchall()

    def drop(self):
        self.cursor.execute("DROP TABLE loaders")
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

@click.command()
@click.option("-m", type=str, help="commit name", default="")
@click.option("--add", type=str, help="add loader origin (agit --add \"origin master\")", default="")
@click.option("--clear", is_flag=True, help="clear origins")
@click.option("-n", type=int, help="origin number", default=1)
@click.option("-s", is_flag=True, help="show origins")
def main(m, add, clear, n, s):
    db = InfoDB()
    if (clear):
        db.drop()
    if (add):
        db.add(add)
    if (s):
        origins = db.get()
        if (not len(origins)):
            print("No available origins")
        else:
            for i, origin in enumerate(origins):
                print(f"{i+1}: {origin[0]}")
    if (m):
        origins = db.get()
        if (n > 0 and n <= len(origins)):
            s = subprocess.Popen("git add .", shell=True)
            s.wait()
            s = subprocess.Popen(f'git commit -m "{m}"', shell=True)
            s.wait()
            s = subprocess.Popen(f"git push {origins[n-1][0]}", shell=True)
            s.wait()
        else:
            if (n != 1):
                print(f"Error: Invalid value for '-n': '{n}' is out of range.")
            else:
                print(f"Create new origin. Example")
                print("  agit --add \"origin master\"")
        print("Nothing to do. Print '--help'")

if __name__ == "__main__":
    main()
