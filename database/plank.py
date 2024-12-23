class Plank:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def create_table(self):
        """Maak de tabel Plank aan."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Plank (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nummer INTEGER NOT NULL,
                boekenwand_id INTEGER,
                FOREIGN KEY (boekenwand_id) REFERENCES Boekenwand(id)
            )
        ''')
        self.conn.commit()
