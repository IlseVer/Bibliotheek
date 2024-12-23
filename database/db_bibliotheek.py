import sqlite3

from database.boek import Boek
from database.auteur import Auteur
from database.genre import Genre
from database.genre_boek import GenreBoek
from database.boek_auteur import BoekAuteur
from database.beschikbaarheid import Beschikbaarheid
from database.boekenwand import Boekenwand
from database.plank import Plank

class DbBibliotheek:
    def __init__(self, database_file):
        self.database_file = database_file
        self.conn = None
        self.cursor = None

        # Pverbinding proberen te maken met de database
        try:
            self.conn = sqlite3.connect(self.database_file)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()

            # Controleren of de tabellen al bestaan
            if not self.tables_exist():
                print("Tabellen worden aangemaakt...")
                self.create_tables()
            else:
                print("Verbonden met de database.")

        except Exception as e:
            print(f"Fout bij het verbinden met de database: {e}")
            # Als de verbinding niet lukt, tabellen aanmaken
            self.create_tables()

    def tables_exist(self):
        """Controleren of de tabellen al bestaan in de database."""
        tabelnamen = ['Boek', 'Auteur', 'Genre', 'Genre_Boek', 'Boek_Auteur', 'Beschikbaarheid', 'Boekenwand', 'Plank']

        for tabel in tabelnamen:
            query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tabel}';"
            self.cursor.execute(query)
            if not self.cursor.fetchone():
                return False  # Als een van de tabellen niet bestaat, geef False terug

        return True  # Alle tabellen bestaan al

    def create_tables(self):
        """alle tabellen aanmaken in de database."""
        # nieuwe verbinding aanmaken om tabellen aan te maken
        self.conn = sqlite3.connect(self.database_file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.db_auteur = Auteur(self.conn)
        self.db_boek = Boek(self.conn)
        self.db_genre = Genre(self.conn)
        self.db_genre_boek = GenreBoek(self.conn)
        self.db_boek_auteur = BoekAuteur(self.conn)
        self.db_beschikbaarheid = Beschikbaarheid(self.conn)
        self.db_boekenwand = Boekenwand(self.conn)
        self.db_plank = Plank(self.conn)

        # tabellen aanmaken
        self.db_auteur.create_table()
        self.db_boek.create_table()
        self.db_genre.create_table()
        self.db_genre_boek.create_table()
        self.db_boek_auteur.create_table()
        self.db_beschikbaarheid.create_table()
        self.db_boekenwand.create_table()
        self.db_plank.create_table()
        print("Tabellen aangemaakt.")

    def close_connection(self):
        """databaseverbinding sluiten."""
        if self.conn:
            self.conn.close()

# Testen
if __name__ == "__main__":
    db = DbBibliotheek('bibliotheek.db')
    db.close_connection()