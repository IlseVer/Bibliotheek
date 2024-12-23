class Genre:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def create_table(self):
        """tabel Genre aanmaken."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Genre (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                naam TEXT NOT NULL UNIQUE
            )
        ''')
        self.conn.commit()

