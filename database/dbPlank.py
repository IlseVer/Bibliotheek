class Plank:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def create_table(self):
        """Maak de tabel Plank aan."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Plank (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nummer INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def get_all_planks(self):
        """Haal alle planken op."""
        self.cursor.execute("SELECT * FROM Plank")
        return self.cursor.fetchall()




