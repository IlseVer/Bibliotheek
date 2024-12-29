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
        plt.yticks([int(y) for y in plt.yticks()[0]])  # om op de y-as gehele getallen te hebben zonder een extra package te installeren (y-ticks converteren naar gehele getallen
        plt.title('Boekverdeling per genre')
        plt.xticks(rotation=45)
        plt.tight_layout() # voor ruimte tussen de labels, anders komen mijn labels buiten beeld
        plt.show()

    def plot_publication_years(self):
        boeken = self.boek_model.get_all_books()
        years = [boek['publicatiejaar'] for boek in boeken]

        # Histogram
        plt.hist(years, bins=range(min(years), max(years) + 1, 1), edgecolor='black', color='green')
        plt.xlabel('Publicatiejaar')
        plt.ylabel('Aantal boeken')
        plt.yticks([int(y) for y in plt.yticks()[0]])  # om op de y-as gehele getallen te hebben zonder een extra package te installeren (y-ticks converteren naar gehele getallen
        plt.grid(axis='y', linestyle='-', color='grey', linewidth=0.2) # raster, duidelijker
        plt.title('Aantal boeken per publicatiejaar')
        plt.xticks(range(min(years), max(years) + 1, 1), rotation=45)
        plt.tight_layout()
        plt.show()
