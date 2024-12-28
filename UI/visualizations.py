import matplotlib.pyplot as plt

class BookVisualizer:
    def __init__(self, genre_model, boek_model, beschikbaarheid_model):
        self.genre_model = genre_model
        self.boek_model = boek_model
        self.beschikbaarheid_model = beschikbaarheid_model

    def plot_genre(self):
        genres = self.genre_model.get_all_genres()
        genre_counts = {genre['genre']: 0 for genre in genres}

        boeken = self.boek_model.get_all_books()
        for boek in boeken:
            genre = self.genre_model.get_genre_by_id(boek['genre_id'])
            if genre:
                genre_counts[genre['genre']] += 1

        # Bar chart
        plt.bar(genre_counts.keys(), genre_counts.values())
        plt.xlabel('Genres')
        plt.ylabel('Aantal boeken')
        plt.title('Boekverdeling per genre')
        plt.xticks(rotation=45)
        plt.tight_layout() # voor ruimte tussen de labels, anders komen mijn labels buiten beeld
        plt.show()

    def plot_publication_years(self):
        boeken = self.boek_model.get_all_books()
        year_counts = {}

        # Het aantal boeken per publicatiejaar tellen
        for boek in boeken:
            year = boek['publicatiejaar']
            if year in year_counts:
                year_counts[year] += 1
            else:
                year_counts[year] = 1

        # Jaren sorteren en het aantal boeken per jaar
        years = sorted(year_counts.keys())
        counts = [year_counts[year] for year in years]

        # Lijngrafiek
        plt.plot(years, counts, marker='o', color='blue', linewidth=2)
        plt.xlabel('Publicatiejaar')
        plt.ylabel('Aantal boeken')
        plt.title('Aantal boeken per publicatiejaar')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
