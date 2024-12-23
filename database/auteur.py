class Auteur:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def create_table(self):
        """tabel Auteur aanmaken."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Auteur (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naam TEXT NOT NULL,
                voornaam TEXT NOT NULL
            )
        ''')
        self.conn.commit()

