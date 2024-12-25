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

    def get_all_planks(self):
        """Haal alle planken op."""
        self.cursor.execute("SELECT * FROM Plank")
        return self.cursor.fetchall()

    def add_defaults_planks(self):
        self.cursor.execute("SELECT nummer FROM Plank WHERE nummer IN ('A', 'B', 'C')")
        bestaande_planken = set(row[0] for row in self.cursor.fetchall())

        # Voeg de planken A, B, C toe als ze nog niet bestaan
        planken = ['A', 'B', 'C']
        for nummer in planken:
            if nummer not in bestaande_planken:
                self.cursor.execute("INSERT INTO Plank (nummer) VALUES (?)", (nummer,))
        self.conn.commit()


