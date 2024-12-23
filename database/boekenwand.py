class Boekenwand:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def create_table(self):
        """tabel Boekenwand aanmaken."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Boekenwand (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naam TEXT NOT NULL UNIQUE
            )
        ''')
        self.conn.commit()
