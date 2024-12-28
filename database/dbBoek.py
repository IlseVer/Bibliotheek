class Boek:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def create_table(self):
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

    def get_book_by_id(self, boek_id):
        query = """
        SELECT Boek.*, Plank.nummer as plank_nummer, 
               Beschikbaarheid.status, Genre.naam as genre_naam
        FROM Boek
        LEFT JOIN Plank ON Boek.plank_id = Plank.id
        LEFT JOIN Beschikbaarheid ON Boek.beschikbaarheid_id = Beschikbaarheid.id
        LEFT JOIN Genre ON Boek.genre_id = Genre.id
        WHERE Boek.id = ?
        """
        self.cursor.execute(query, (boek_id,))
        return self.cursor.fetchone()

    #titel bijwerken
    def update_book(self, boek_id, nieuwe_titel):
        query = "UPDATE Boek SET titel = ? WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (nieuwe_titel, boek_id))
        self.conn.commit()

    # status beschikbaarheid bijwerken
    def update_boek_beschikbaarheid(self, boek_id, beschikbaarheid_id):
        query = "UPDATE Boek SET beschikbaarheid_id = ? WHERE id = ?"
        self.cursor.execute(query, (beschikbaarheid_id, boek_id))
        self.conn.commit()
        print(f"Beschikbaarheid van boek met ID {boek_id} is bijgewerkt.")


    def update_boek_genre(self, boek_id, genre_id):
        query = "UPDATE Boek SET genre_id = ? WHERE id = ?"
        self.cursor.execute(query, (genre_id, boek_id))
        self.conn.commit()
        print(f"Genre van boek met ID {boek_id} is bijgewerkt.")

    def update_boek_plank(self, boek_id, plank_id):
        self.cursor.execute("UPDATE Boek SET plank_id = ? WHERE id = ?", (plank_id, boek_id))
        self.conn.commit()

    def delete_boek(self, boek_id):
        query = "DELETE FROM Boek WHERE id = ?"
        self.cursor.execute(query, (boek_id,))
        self.conn.commit()

