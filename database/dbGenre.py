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

    def add_genre_if_not_exists(self, genre_name):
        query_select = "SELECT id FROM genres WHERE genre = ?"
        query_insert = "INSERT INTO genres (genre) VALUES (?)"
        cursor = self.conn.cursor()

        # Controleer of het genre al bestaat
        cursor.execute(query_select, (genre_name,))
        result = cursor.fetchone()

        if result:  # Bestaat al
            return result['id']
        else:  # Voeg een nieuw genre toe
            cursor.execute(query_insert, (genre_name,))
            self.conn.commit()
            return cursor.lastrowid

