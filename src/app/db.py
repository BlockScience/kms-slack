import sqlite3
from app.config import DB_PATH


class Preferences:
    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()
        self._execute(
            "CREATE TABLE IF NOT EXISTS users (user_id TEXT NOT NULL PRIMARY KEY, dm_mode TEXT)"
        )

    def set_dm_mode(self, user_id: str, dm_mode: str) -> None:
        self._execute("REPLACE INTO users VALUES (?, ?)", (user_id, dm_mode))

    def get_dm_mode(self, user_id: str) -> str | None:
        r = self._execute("SELECT dm_mode FROM users WHERE user_id = ?", (user_id,))
        return None if len(r) < 1 else r[0][0]

    def _execute(self, query, params=(None)):
        if params:
            c = self.cursor.execute(query, params)
        else:
            c = self.cursor.execute(query)
        self.connection.commit()
        return c.fetchall()
