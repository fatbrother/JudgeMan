import sqlite3
import json

class ProblemSet:
    def __init__(self, db: str):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS problemSet (id INTEGER PRIMARY KEY, title text, problems text)")
        self.conn.commit()

    def insert(self, title: str, problems: list):
        problemsId = json.dumps(problems)
        self.cur.execute("INSERT INTO problemSet VALUES (NULL, ?, ?)", (title, problemsId))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM problemSet")
        rows = self.cur.fetchall()

        for row in rows:
            row['problems'] = json.loads(row['problems'])

        return rows

    def search(self, id=0, title="", problems=""):
        self.cur.execute("SELECT * FROM problemSet WHERE id=? OR title=? OR problems=?", (id, title, problems))
        rows = self.cur.fetchall()

        for row in rows:
            row['problems'] = json.loads(row['problems'])

        return rows

    def delete(self, id: int):
        self.cur.execute("DELETE FROM problemSet WHERE id=?", (id))
        self.conn.commit()

    def update(self, id: int, title: str, problems: list):
        problemsId = json.dumps(problems)
        self.cur.execute("UPDATE problemSet SET title=?, problems=? WHERE id=?", (title, problemsId, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()