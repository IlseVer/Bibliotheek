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
                FOREIGN KEY (locatie) REFERENCES Plank(id),
                FOREIGN KEY (beschikbaarheid_id) REFERENCES Beschikbaarheid(id)
            )
        ''')
        self.conn.commit()

    def add_boek(self, titel, publicatiejaar, locatie, beschikbaarheid_id):
        """Voeg een nieuw boek toe aan de database."""
        self.cursor.execute("""
            INSERT INTO Boek (titel, publicatiejaar, locatie, beschikbaarheid_id) 
            VALUES (?, ?, ?, ?)
        """, (titel, publicatiejaar, locatie, beschikbaarheid_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_books(self):
        """Haal alle boeken op met hun locatie en beschikbaarheid."""
        self.cursor.execute("""
            SELECT Boek.*, Plank.nummer as plank_nummer, Beschikbaarheid.status 
            FROM Boek 
            LEFT JOIN Plank ON Boek.locatie = Plank.id
            LEFT JOIN Beschikbaarheid ON Boek.beschikbaarheid_id = Beschikbaarheid.id
        """)
        return self.cursor.fetchall()



