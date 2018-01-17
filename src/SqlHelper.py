import sqlite3


class SqlHelper:

    def __init__(self):
        self.connection = sqlite3.connect('seeYaLater.db')
        self.prepareDatabase()

    def prepareDatabase(self):
        self.execute("""
            CREATE TABLE IF NOT EXISTS departure (
            id INT NOT NULL PRIMARY KEY,
            line VARCHAR(4),
            direction VARCHAR(42),
            realTime DATETIME,
            scheduledTime DATETIME,
            station INT
            )
        """)

    def execute(self, sql_command: str):
        cursor = self.connection.cursor()
        cursor.execute(sql_command)
        self.connection.commit()
        return cursor.fetchone()
