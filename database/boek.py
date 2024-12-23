class Boek:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def create_table(self):
        """tabel Boek aanmaken."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Boek (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titel TEXT NOT NULL,
                publicatiejaar INTEGER NOT NULL,
                locatie INTEGER,
                beschikbaarheid_id INTEGER,
                FOREIGN KEY (locatie) REFERENCES Plank(id),
                FOREIGN KEY (beschikbaarheid_id) REFERENCES Beschikbaarheid(id)
            )
        ''')
        self.conn.commit()


