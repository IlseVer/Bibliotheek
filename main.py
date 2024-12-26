import datetime
import sys
import csv
import pandas as pd

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
        print("\n1: Voeg boek toe")
        print("2: Toon alle boeken")
        print("3: Zoek boeken")
        print("4: Beheer genres")
        print("5: Wijzig gegevens")
        print("6: Exporteer boekenlijst naar Excel of csv")
        print("7: Sluit het programma")
        keuze = input("Maak een keuze: ").strip().lower()

        # 1: VOEG BOEK TOE
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

            #controleren als er al genres aanwezig zijn
            genres = genre_model.get_all_genres()
            #GEEN genres aanwezig:
            if not genres:
                print("Er zijn nog geen genres. Maak eerst een genre aan.")
                while True:
                    nieuw_genre = input("Voer de naam van het nieuwe genre in: ")
                    if nieuw_genre.strip():
                        genre_id = genre_model.add_genre_if_not_exists(nieuw_genre)
                        print(f"Genre '{nieuw_genre}' toegevoegd met ID {genre_id}.")
                        break
                    else:
                        print("Genre naam mag niet leeg zijn. Probeer opnieuw.")

            # WEl genres aanwezig
            else:
                print("\nBeschikbare genres:")
                for genre in genres:
                    print(f"{genre['id']}: {genre['genre']}")

                while True:
                    try:
                        genre_id = int(input("Kies een genre ID (of 0 om een nieuw genre toe te voegen): "))
                        if genre_id == 0:
                            nieuw_genre = input("Voer de naam van het nieuwe genre in: ")
                            genre_id = genre_model.add_genre_if_not_exists(nieuw_genre)
                            if genre_id:
                                print(f"Genre '{nieuw_genre}' is toegevoegd.")
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
                print(f"{status['id']}: {status['status']}")

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
            print(f"Boek '{titel}' is succesvol toegevoegd aan de bibliotheek")

            # auteur koppelen aan boek
            boek_auteur_model.add_boek_auteur(boek_id, auteur_id)

        # 2: TOON ALLE BOEKEN
        elif keuze == '2':
            boeken = boek_model.get_all_books()
            print("\nAlle boeken:")
            for boek in boeken:
                # naam van de auteur ophalen via het auteur_id
                auteur = auteur_model.get_auteur_by_id(boek['auteur_id'])
                auteur_naam = f"{auteur['voornaam']} {auteur['naam']}" if auteur else "Onbekend"

                print(f"{boek['id']}) {boek['titel']}, Auteur: {auteur_naam}, Jaar: {boek['publicatiejaar']}")
                print(f"Plank {boek['plank_nummer'] or 'Geen'}, Status: {boek['status']}")
                print("-" * 50)

        # 3: ZOEK Boeken (1: op titel of 2:op genre)
        elif keuze == '3':
            while True:
                print("\nZoekmenu:")
                print("1: Zoek op titel")
                print("2: Zoek op genre")
                print("3: Ga terug naar hoofdmenu")
                print("4: exit")
                subkeuze = input("Maak een keuze: ")

                if subkeuze == '1':
                    zoekterm = input("Voer de titel (of deel van de titel) in: ")
                    resultaten = boek_model.search_books_by_title(zoekterm)

                    if resultaten:
                        print(f"\nZoekresultaten voor titel '{zoekterm}':")
                        for boek in resultaten:
                            auteur = auteur_model.get_auteur_by_id(boek['auteur_id'])
                            auteur_naam = f"{auteur['voornaam']} {auteur['naam']}" if auteur else "Onbekend"
                            print(f"{boek['id']}) {boek['titel']}, Auteur: {auteur_naam}, Jaar: {boek['publicatiejaar']}")
                            print(f"Plank {boek['plank_nummer'] or 'Geen'}, Status: {boek['status']}")
                            print("-" * 50)
                    else:
                        print(f"Geen titel gevonden met de zoekterm '{zoekterm}'")

                elif subkeuze == '2':
                    zoekterm = input("Voer een genre in (of een deel ervan, bijv. 'thr' voor 'thriller'): ")
                    resultaten = boek_model.search_books_by_genre(zoekterm)

                    if resultaten:
                        print(f"\nZoekresultaten voor genre '{zoekterm}':")
                        for boek in resultaten:
                            auteur = auteur_model.get_auteur_by_id(boek['auteur_id'])
                            auteur_naam = f"{auteur['voornaam']} {auteur['naam']}" if auteur else "Onbekend"
                            genre = boek['genre_naam']
                            print(
                                f"{boek['id']}) {boek['titel']}, Auteur: {auteur_naam}, Genre: {genre}, Jaar: {boek['publicatiejaar']}")
                            print(f"Plank {boek['plank_nummer'] or 'Geen'}, Status: {boek['status']}")
                            print("-" * 50)


                elif subkeuze == '3':
                    break

                elif subkeuze == '4' or subkeuze == 'exit':
                    print("Programma wordt afgesloten...")
                    print("Programma afgesloten.")
                    sys.exit()
                else:
                    print("Ongeldige keuze, probeer opnieuw.")

        # 4: BEHEER GENRES
        elif keuze == '4':
            while True:
                print("\nGenremenu:")
                print("1. Voeg een nieuw genre toe")
                print("2. Toon alle genres")
                print("3. Wijzig een genre")
                print("4. Ga terug naar hoofdmenu")
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
                    print("-" * 50)
                    print("Alle genres:")

                    for genre in genres:
                        print(f"{genre['id']}. {genre['genre']}")
                    print("-" * 50)

                elif subkeuze == '3':  # Optie voor het wijzigen van een genre
                    genres = genre_model.get_all_genres()
                    print("-" * 50)
                    print("Beschikbare genres om te wijzigen:")

                    for genre in genres:
                        print(f"{genre['id']}. {genre['genre']}")
                    print("-" * 50)

                    try:
                        genre_id = int(input("Voer het ID van het genre in dat je wilt wijzigen: "))
                        genre = genre_model.get_genre_by_id(genre_id)  # Haal het genre op via het ID
                        if genre:
                            nieuwe_naam = input(f"Huidige naam: {genre['genre']}\nVoer de nieuwe naam in: ").strip()
                            if nieuwe_naam:
                                genre_model.update_genre(genre_id, nieuwe_naam)
                                print(f"Genre is succesvol gewijzigd naar: {nieuwe_naam}")
                            else:
                                print("Nieuwe naam mag niet leeg zijn.")
                        else:
                            print(f"Geen genre gevonden met ID {genre_id}.")
                    except ValueError:
                        print("Ongeldige invoer. Kies een geldig genre ID.")

                elif subkeuze == '4':
                    break

                else:
                    print("Ongeldige keuze, probeer opnieuw.")


        # 5: WIJZIG GEGEVENS
        elif keuze == '5':
            boeken = boek_model.get_all_books()
            print("\nBeschikbare boeken:")
            for boek in boeken:
                print(f"{boek['id']}: {boek['titel']}")

            try:
                boek_id = int(input("\nKies het ID van het boek dat je wilt wijzigen: "))
                boek = boek_model.get_book_by_id(boek_id)

                if boek:
                    print(f"\nBoek: {boek['titel']} ({boek['publicatiejaar']})")
                    auteur = auteur_model.get_auteur_by_id(boek['auteur_id'])
                    print(f"Auteur: {auteur['voornaam']} {auteur['naam']}")
                    print(f"Genre: {boek['genre_naam']}")
                    print(f"Plank: {boek['plank_nummer'] if boek['plank_nummer'] else 'Geen'}")
                    print(f"Beschikbaarheid: {boek['status']}")

                    # Vraag wat ze willen aanpassen
                    print("\nWat wil je aanpassen?")
                    print("1. Titel")
                    print("2. Genre")
                    print("3. Beschikbaarheid")
                    print("4. plaats (plank)")
                    print("5. Ga terug naar hoofdmenu")
                    wijzig_keuze = input("Maak een keuze: ")

                    if wijzig_keuze == '1':  # Titel aanpassen
                        nieuwe_titel = input(f"Huidige titel: {boek['titel']}\nVoer de nieuwe titel in: ").strip()
                        if nieuwe_titel:
                            boek_model.update_book(boek_id, nieuwe_titel)
                            print(f"Boek titel gewijzigd naar: {nieuwe_titel}")

                    elif wijzig_keuze == '2':  # Genre aanpassen
                        genres = genre_model.get_all_genres()
                        print("\nBeschikbare genres:")
                        for genre in genres:
                            print(f"{genre['id']}: {genre['genre']}")

                        genre_id = int(input("Kies het ID van het nieuwe genre: "))
                        if any(g['id'] == genre_id for g in genres):
                            boek_model.update_boek_genre(boek_id, genre_id)
                            print(f"Genre gewijzigd naar: {genre_model.get_genre_by_id(genre_id)['genre']}")

                    elif wijzig_keuze == '3':  # Beschikbaarheid aanpassen
                        statussen = beschikbaarheid_model.get_all_statuses()
                        print("\nBeschikbare statussen:")
                        for status in statussen:
                            print(f"{status['id']}: {status['status']}")

                        beschikbaarheid_id = int(input("Kies het ID van de nieuwe beschikbaarheid: "))
                        if any(s['id'] == beschikbaarheid_id for s in statussen):
                            boek_model.update_boek_beschikbaarheid(boek_id, beschikbaarheid_id)
                            print(
                                f"Beschikbaarheid gewijzigd naar: {beschikbaarheid_model.get_all_statuses()[beschikbaarheid_id - 1]['status']}")

                    elif wijzig_keuze == '4':  # Plank aanpassen
                        planken = plank_model.get_all_planks()
                        print("\nBeschikbare planken:")
                        for plank in planken:
                            print(f"{plank['id']}: Plank {plank['nummer']}")

                        while True:
                            try:
                                plank_id = int(input("Kies het ID van de nieuwe plank (of 0 voor geen locatie): "))
                                if plank_id == 0:
                                    plank_id = None
                                elif not any(p['id'] == plank_id for p in planken):
                                    print("Ongeldige plank ID")
                                    continue
                                break
                            except ValueError:
                                print("Voer een geldig nummer in")

                        # Werk de plank bij voor het boek
                        boek_model.update_boek_plank(boek_id, plank_id)
                        print(f"Plank gewijzigd naar: {plank_id if plank_id else 'Geen'}")


                    elif wijzig_keuze == '5':  # Terug naar hoofdmenu
                        break
                    else:
                        print("Ongeldige keuze, probeer opnieuw.")
                else:
                    print("Geen boek gevonden met dat ID.")
            except ValueError:
                print("Ongeldige invoer. Kies een geldig boek ID.")


        # 6: Exporteer boekenlijst naar Excel
        elif keuze == '6':
            while True:
                print("\nWelk formaat wenst u de exporteren?")
                print("1: CSV")
                print("2: Excel")
                print("3: Ga terug naar hoofdmenu")
                print("4: exit")
                subkeuze = input("Maak een keuze: ")

                if subkeuze == '1':
                    try:
                        # boekenlijst ophalen
                        boeken = boek_model.get_all_books()

                        # timestamp
                        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hu%M')
                        bestandsnaam = f'boekenlijst_{timestamp}.csv'

                        # Open het CSV bestand voor schrijven
                        with open(bestandsnaam, 'w', newline='', encoding='utf-8') as csvfile:
                            veldnamen = ['Titel', 'Auteur', 'Publicatiejaar', 'Plank', 'Status', 'Genre']
                            writer = csv.DictWriter(csvfile, fieldnames=veldnamen)

                            writer.writeheader()  # Schrijf de header (kolomnamen)

                            # rijen vullen met gegevens
                            for boek in boeken:
                                auteur = auteur_model.get_auteur_by_id(boek['auteur_id'])
                                auteur_naam = f"{auteur['voornaam']} {auteur['naam']}" if auteur else "Onbekend"
                                writer.writerow({
                                    'Titel': boek['titel'],
                                    'Auteur': auteur_naam,
                                    'Publicatiejaar': boek['publicatiejaar'],
                                    'Plank': boek['plank_nummer'] or 'Geen',
                                    'Status': boek['status'],
                                    'Genre': boek['genre_naam']
                                })

                        print(f"Boekenlijst is succesvol geëxporteerd naar '{bestandsnaam}'.")

                    except Exception as e:
                        print(f"Fout bij het exporteren van de boekenlijst: {e}")

                elif subkeuze == '2':
                    try:
                        boeken = boek_model.get_all_books()

                        #timestamp
                        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%Hu%M')
                        bestandsnaam = f'boekenlijst_{timestamp}.xlsx'

                        # lijst van dictionaries voor de boeken maken
                        data = []
                        for boek in boeken:
                            auteur = auteur_model.get_auteur_by_id(boek['auteur_id'])
                            auteur_naam = f"{auteur['voornaam']} {auteur['naam']}" if auteur else "Onbekend"
                            data.append({
                                'Titel': boek['titel'],
                                'Auteur': auteur_naam,
                                'Publicatiejaar': boek['publicatiejaar'],
                                'Plank': boek['plank_nummer'] or 'Geen',
                                'Status': boek['status'],
                                'Genre': boek['genre_naam']
                            })

                        # Maak een DataFrame van de data en schrijf naar een Excel-bestand
                        df = pd.DataFrame(data)
                        df.to_excel(f'{bestandsnaam}.xlsx', index=False, engine='openpyxl')

                        print(f"Boekenlijst is succesvol geëxporteerd naar '{bestandsnaam}'.")

                    except Exception as e:
                        print(f"Fout bij het exporteren van de boekenlijst naar Excel: {e}")

                elif subkeuze == '3':
                    break
                elif subkeuze == '4' or subkeuze == 'exit':
                    print("Programma wordt afgesloten...")
                    print("Programma afgesloten.")
                    sys.exit()
                else:
                    print("Ongeldige keuze, probeer het opnieuw.")

        elif keuze == '7' or keuze == 'exit':
            print("Programma wordt afgesloten...")
            print("Programma afgesloten.")
            sys.exit()
        else:
            print("Ongeldige keuze, probeer het opnieuw.")

if __name__ == "__main__":
    main()