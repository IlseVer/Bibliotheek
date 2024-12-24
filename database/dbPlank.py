class Plank:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def create_table(self):
        """Maak de tabel Plank aan."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Plank (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nummer INTEGER NOT NULL,
                boekenwand_id INTEGER,
                FOREIGN KEY (boekenwand_id) REFERENCES Boekenwand(id)
            )
        ''')
        self.conn.commit()

    def get_all_planks(self):
        """Haal alle planken op met hun boekenwand."""
        self.cursor.execute("""
             SELECT Plank.*, Boekenwand.naam as boekenwand_naam 
             FROM Plank 
             LEFT JOIN Boekenwand ON Plank.boekenwand_id = Boekenwand.id
         """)
        return self.cursor.fetchall()




