class Auteur:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Auteur (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naam TEXT NOT NULL,
                voornaam TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    #Voeg een nieuwe auteur toe.
    def add_auteur(self, naam, voornaam):
        self.cursor.execute("SELECT * FROM Auteur WHERE naam = ? AND voornaam = ?", (naam, voornaam))
        existing_auteur = self.cursor.fetchone()
        if existing_auteur:
            return existing_auteur['id']
        else:
            self.cursor.execute("INSERT INTO Auteur (naam, voornaam) VALUES (?, ?)", (naam, voornaam))
            self.conn.commit()
            auteur_id = self.cursor.lastrowid
            print(f"Auteur {naam} {voornaam} is toegevoegd met ID {auteur_id}.")
            return auteur_id

    def get_all_auteurs(self):
        self.cursor.execute('SELECT * FROM Auteur')
        return self.cursor.fetchall()

    def get_auteur_by_id(self, auteur_id):
        self.cursor.execute('SELECT * FROM Auteur WHERE id = ?', (auteur_id,))
        return self.cursor.fetchone()

