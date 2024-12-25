from database.db_bibliotheek import DbBibliotheek
from database.dbBoek import Boek
from database.dbPlank import Plank
from database.dbBeschikbaarheid import Beschikbaarheid
from database.dbGenre import Genre
from database.dbAuteur import Auteur
from database.boek_auteur import BoekAuteur


def main():
    db = DbBibliotheek('database/bib.db')

    boek_model = Boek(db.conn)
    plank_model = Plank(db.conn)
    beschikbaarheid_model = Beschikbaarheid(db.conn)
    genre_model = Genre(db.conn)
    auteur_model = Auteur(db.conn)
    boek_auteur_model = BoekAuteur(db.conn)

    beschikbaarheid_model.insert_default_values()

    while True:
        print("\n1. Voeg boek toe")
        print("2. Toon alle boeken")
        print("3. Beheer genres")
        print("4. Stop")
        keuze = input("Maak een keuze: ")

        if keuze == '1':
            titel = input("Voer de titel van het boek in: ")
            while True:
                try:
                    publicatiejaar = int(input("Voer het publicatiejaar in: "))
                    break
                except ValueError:
                    print("Voer een geldig jaartal in.")

            # Auteur toevoegen of ophalen
            voornaam = input("Voer de voornaam van de auteur in: ")
            naam = input("Voer de naam van de auteur in: ")
            auteur_id = auteur_model.add_auteur(naam, voornaam)

            genres = genre_model.get_all_genres()
            if not genres:
                print("Er zijn nog geen genres. Maak eerst een genre aan.")
                continue

            # beschikbare genres tonen:
            print("\nBeschikbare genres:")
            for genre in genres:
                print(f"{genre['id']}: Genre {genre['genre']}")

            while True:
                try:
                    genre_id = int(input("Kies een genre ID (of 0 om een nieuw genre toe te voegen): "))
                    if genre_id == 0:
                        nieuw_genre = input("Voer de naam van het nieuwe genre in: ")
                        genre_id = genre_model.add_genre_if_not_exists(nieuw_genre)
                        if genre_id:
                            print(f"Genre '{nieuw_genre}' toegevoegd met ID {genre_id}.")
                    elif not any(g['id'] == genre_id for g in genres):
                        print("Ongeldige genre ID")
                        continue
                    break
                except ValueError:
                    print("Voer een geldig nummer in")


            # Toon beschikbare planken
            planken = plank_model.get_all_planks()
            if not planken:
                plank_model.add_defaults_planks()  # Voeg automatisch planken toe
                planken = plank_model.get_all_planks()  # Haal de planken opnieuw op

            print("\nBeschikbare planken:")
            for plank in planken:
                print(f"{plank['id']}: Plank {plank['nummer']}")

            while True:
                try:
                    plank_id = int(input("Kies een plank (of 0 voor geen locatie): "))
                    if plank_id == 0:
                        plank_id = None
                    elif not any(p['id'] == plank_id for p in planken):
                        print("Ongeldige plank ID")
                        continue
                    break
                except ValueError:
                    print("Voer een geldig nummer in")


            # Toon beschikbaarheidsstatussen
            statussen = beschikbaarheid_model.get_all_statuses()
            print("\nBeschikbare statussen:")
            for status in statussen:
                print(f"ID: {status['id']}, Status: {status['status']}")

            while True:
                try:
                    beschikbaarheid_id = int(input("Kies een status ID: "))
                    if not any(s['id'] == beschikbaarheid_id for s in statussen):
                        print("Ongeldige status ID")
                        continue
                    break
                except ValueError:
                    print("Voer een geldig nummer in")

            # Voeg het boek toe
            boek_id = boek_model.add_boek(titel, publicatiejaar, auteur_id, genre_id, plank_id, beschikbaarheid_id)
            print(f"Boek '{titel}' is toegevoegd met ID {boek_id}")

            # auteur koppelen aan boek
            boek_auteur_model.add_boek_auteur(boek_id, auteur_id)

        elif keuze == '2':
            boeken = boek_model.get_all_books()
            print("\nAlle boeken:")
            for boek in boeken:
                print(f"{boek['id']}) Titel: {boek['titel']}, Jaar: {boek['publicatiejaar']}")
                print(f"Plank: {boek['plank_nummer'] or 'Geen'}, Status: {boek['status']}")
                print("-" * 50)

        elif keuze == '3':
            while True:
                print("\nGenremenu:")
                print("1. Voeg een nieuw genre toe")
                print("2. Toon alle genres")
                print("3. Ga terug naar hoofdmenu")
                subkeuze = input("Maak een keuze: ")

                if subkeuze == '1':
                    nieuw_genre = input("Voer de naam van het nieuwe genre in: ")
                    try:
                        genre_id = genre_model.add_genre_if_not_exists(nieuw_genre)
                        if genre_id:
                            print(f"Genre '{nieuw_genre}' toegevoegd met ID {genre_id}.")
                    except Exception as e:
                        print(f"Fout bij het toevoegen van het genre: {e}")

                elif subkeuze == '2':
                    genres = genre_model.get_all_genres()
                    print("\nAlle genres:")
                    for genre in genres:
                        print(f"ID: {genre['id']}, Naam: {genre['genre']}")
                    print("-" * 50)

                elif subkeuze == '3':
                    break

                else:
                    print("Ongeldige keuze, probeer opnieuw.")

        elif keuze == '4':
            print("Programma wordt afgesloten...")
            print("Programma afgesloten.")
            break
        else:
            print("Ongeldige keuze, probeer het opnieuw.")

    db.close_connection()

if __name__ == "__main__":
    main()