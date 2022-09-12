import sqlite3

class Problems:
    def __init__(self, db: str) -> None:
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS problems (id INTEGER PRIMARY KEY, title text, description text, testCaseNumber integer)")
        self.conn.commit()

    def insert(self, title: str, description: str, testCaseNumber: int) -> None:
        self.cur.execute("INSERT INTO problems VALUES (NULL, ?, ?, ?)", (title, description, testCaseNumber))
        self.conn.commit()

    def view(self) -> list:
        self.cur.execute("SELECT * FROM problems") 
        rows = self.cur.fetchall()
        return rows

    def search(self, id=0) -> list:
        self.cur.execute("SELECT * FROM problems WHERE id=?", (id))
        rows = self.cur.fetchall()
        return rows

    def delete(self, id: int) -> None:
        self.cur.execute("DELETE FROM problems WHERE id=?", (id))
        self.conn.commit()

    def update(self, id: int, title: str, description: str, testCaseNumber: int) -> None:
        self.cur.execute("UPDATE problems SET title=?, description=?, testCaseNumber=? WHERE id=?", (title, description, testCaseNumber, id))
        self.conn.commit()

    def __del__(self) -> None:
        self.conn.close()