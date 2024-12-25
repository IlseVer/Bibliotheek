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
                auteur_id INTEGER NOT NULL,
                genre_id INTEGER NOT NULL,
                plank_id INTEGER,
                beschikbaarheid_id INTEGER,
                FOREIGN KEY (auteur_id) REFERENCES Auteur(id),
                FOREIGN KEY (genre_id) REFERENCES Genre(id),
                FOREIGN KEY (plank_id) REFERENCES Plank(id),
                FOREIGN KEY (beschikbaarheid_id) REFERENCES Beschikbaarheid(id)
            )
        ''')
        self.conn.commit()

    def add_boek(self, titel, publicatiejaar, auteur_id, genre_id, plank_id, beschikbaarheid_id):
        self.cursor.execute("""
            INSERT INTO Boek (titel, publicatiejaar, auteur_id, genre_id, plank_id, beschikbaarheid_id) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (titel, publicatiejaar, auteur_id, genre_id, plank_id, beschikbaarheid_id))
        self.conn.commit()
        return self.cursor.lastrowid

    #alle boeken ophalen met hun locatie en beschikbaarheid
    def get_all_books(self):
        self.cursor.execute("""
            SELECT Boek.*, Plank.nummer as plank_nummer, Beschikbaarheid.status , Genre.naam as genre_naam
            FROM Boek 
            LEFT JOIN Plank ON Boek.plank_id = Plank.id
            LEFT JOIN Beschikbaarheid ON Boek.beschikbaarheid_id = Beschikbaarheid.id
            LEFT JOIN Genre ON Boek.genre_id = Genre.id
        """)
        return self.cursor.fetchall()

    def search_books_by_title(self, title):
        """Zoek boeken op basis van de titel."""
        query = """
        SELECT Boek.*, Plank.nummer as plank_nummer, Beschikbaarheid.status
        FROM Boek
        LEFT JOIN Plank ON Boek.plank_id = Plank.id
        LEFT JOIN Beschikbaarheid ON Boek.beschikbaarheid_id = Beschikbaarheid.id
        WHERE LOWER(Boek.titel) LIKE LOWER(?)
        """
        title_pattern = f"%{title}%"
        self.cursor.execute(query, (title_pattern,))
        return self.cursor.fetchall()

    def search_books_by_genre(self, genre):
        """Zoek boeken op basis van het genre."""
        genre_pattern = f"%{genre.lower()}%"  # Zorgen dat de input case-insensitive wordt behandeld
        self.cursor.execute("""
            SELECT Boek.*, Plank.nummer as plank_nummer, Beschikbaarheid.status, Genre.naam as genre_naam
            FROM Boek
            LEFT JOIN Plank ON Boek.plank_id = Plank.id
            LEFT JOIN Beschikbaarheid ON Boek.beschikbaarheid_id = Beschikbaarheid.id
            LEFT JOIN Genre ON Boek.genre_id = Genre.id
            WHERE LOWER(Genre.naam) LIKE ?
        """, (genre_pattern,))

        resultaten = self.cursor.fetchall()

        if not resultaten:
            print(f"Geen boeken gevonden voor genre '{genre}'")
        return resultaten




