class Beschikbaarheid:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def create_table(self):
        """tabel Beschikbaarheid aanmaken."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Beschikbaarheid (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT NOT NULL UNIQUE            
            )
        ''')
        self.conn.commit()

    def get_all_statuses(self):
        self.cursor.execute('SELECT * FROM Beschikbaarheid')
        return self.cursor.fetchall()

    #Indien tabel nog geen statussen bevat:
    def add_status(self, status):
        self.cursor.execute('''
            INSERT OR IGNORE INTO Beschikbaarheid (status) 
            VALUES (?)
        ''', (status,))
        self.conn.commit()

    #Defaultwaarden invoegen
    def insert_default_values(self):
        self.cursor.execute('SELECT COUNT(*) FROM Beschikbaarheid')
        count = self.cursor.fetchone()[0]

        if count == 0:  # Alleen toevoegen als er nog geen gegevens zijn
            self.add_status('Beschikbaar')
            self.add_status('Uitgeleend')
            self.add_status('Zoek')