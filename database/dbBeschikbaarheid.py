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