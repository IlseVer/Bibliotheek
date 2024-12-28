class Genre:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
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
        query_select = "SELECT id FROM Genre WHERE naam = ?"
        query_insert = "INSERT INTO Genre (naam) VALUES (?)"
        cursor = self.conn.cursor()

        # Controleren of het genre al bestaat
        cursor.execute(query_select, (genre_name,))
        result = cursor.fetchone()

        if result:  # Bestaat al
            print(f"Het genre '{genre_name}' bestaat al.")
            return result['id']
        else:  # Voeg een nieuw genre toe
            cursor.execute(query_insert, (genre_name,))
            self.conn.commit()
            print(f"Genre '{genre_name}' is succesvol toegevoegd.")
            return cursor.lastrowid

    def get_genre_by_id(self, genre_id):
        # Haal het genre op via het ID
        query = "SELECT * FROM Genre WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (genre_id,))
        result = cursor.fetchone()  # Haal één resultaat op (de eerste match)

        if result:
            return {'id': result[0], 'genre': result[1]}
        else:
            return None

    # naam genre bijwerken
    def update_genre(self, genre_id, nieuwe_naam):
        query = "UPDATE Genre SET naam = ? WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (nieuwe_naam, genre_id))
        self.conn.commit()

