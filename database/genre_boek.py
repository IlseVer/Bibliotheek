class GenreBoek:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def create_table(self):
        """tussenliggende tabel GenreBoek aanmaken."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Genre_Boek (
                boek_id INTEGER,
                genre_id INTEGER,
                PRIMARY KEY (boek_id, genre_id),
                FOREIGN KEY (boek_id) REFERENCES Boek(id),
                FOREIGN KEY (genre_id) REFERENCES Genre(id)
            )
        ''')
        self.conn.commit()
