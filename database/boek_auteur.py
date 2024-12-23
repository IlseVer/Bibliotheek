class BoekAuteur:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def create_table(self):
        """tussenliggende tabel BoekAuteur aanmaken."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Boek_Auteur (
                boek_id INTEGER,
                auteur_id INTEGER,
                PRIMARY KEY (boek_id, auteur_id),
                FOREIGN KEY (boek_id) REFERENCES Boek(id),
                FOREIGN KEY (auteur_id) REFERENCES Auteur(id)
            )
        ''')
        self.conn.commit()

