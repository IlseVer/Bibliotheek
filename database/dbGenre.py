import sqlite3

class Genre:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """tabel Genre aanmaken."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Genre (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naam TEXT NOT NULL UNIQUE
            )
        ''')
        self.conn.commit()

    # alle genres ophalen en ze terug geven in een lijst van dictionaries
    def get_all_genres(self):
        self.cursor.execute('SELECT * FROM Genre')
        rows = self.cursor.fetchall()
        # Zet elke tuple om naar een dictionary met de juiste sleutels
        genres = [{'id': row[0], 'genre': row[1]} for row in rows]
        return genres

    def add_genre_if_not_exists(self, naam):
        self.cursor.execute("SELECT * FROM Genre WHERE naam = ?", (naam,))
        existing_genre = self.cursor.fetchone()

        if existing_genre:
            print(f"Genre '{naam}' bestaat al in de database.")
            return None
        else:
            try:
                self.cursor.execute("INSERT INTO Genre (naam) VALUES (?)", (naam,))
                self.conn.commit()  # Zorgt ervoor dat de wijziging wordt doorgevoerd
                genre_id = self.cursor.lastrowid  # Haalt het ID op van het toegevoegde genre
                return genre_id
            except sqlite3.IntegrityError as e:
                print(f"Genre '{naam}' kon niet worden toegevoegd door een fout: {e}")
                return None