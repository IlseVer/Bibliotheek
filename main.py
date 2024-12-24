from database.db_bibliotheek import DbBibliotheek
from database.dbBoek import Boek
from database.dbPlank import Plank
from database.dbBeschikbaarheid import Beschikbaarheid

# er moeten statussen bestaan
def setup_beschikbaarheid(beschikbaarheid_model):
    statussen = beschikbaarheid_model.get_all_statuses()
    if not statussen:
        basis_statussen = ["Beschikbaar", "Uitgeleend", "In Restauratie", "Zoek"]
        for status in basis_statussen:
            beschikbaarheid_model.add_status(status)


def main():
    db = DbBibliotheek('database/bibliotheek.db')

    boek_model = Boek(db.conn)
    plank_model = Plank(db.conn)
    beschikbaarheid_model = Beschikbaarheid(db.conn)

    # beschikbaarheidsstatussen
    setup_beschikbaarheid(beschikbaarheid_model)

    while True:
        print("\n1. Voeg boek toe")
        print("2. Toon alle boeken")
        print("3. Stop")
        keuze = input("Maak een keuze: ")

        if keuze == '1':
            titel = input("Voer de titel van het boek in: ")
            while True:
                try:
                    publicatiejaar = int(input("Voer het publicatiejaar in: "))
                    break
                except ValueError:
                    print("Voer een geldig jaartal in.")

            # Toon beschikbare planken
            planken = plank_model.get_all_planks()
            if not planken:
                print("Er zijn nog geen planken beschikbaar. Maak eerst een plank aan.")
                continue

            print("\nBeschikbare planken:")
            for plank in planken:
                print(f"ID: {plank['id']}, Plank {plank['nummer']}",
                      f"(Boekenwand: {plank['boekenwand_naam']})" if plank['boekenwand_naam'] else "")

            while True:
                try:
                    planknummer = int(input("Kies een plank ID (of 0 voor geen locatie): "))
                    if planknummer == 0:
                        planknummer = None
                    elif not any(p['id'] == planknummer for p in planken):
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
            boek_id = boek_model.add_boek(titel, publicatiejaar, planknummer, beschikbaarheid_id)
            print(f"Boek '{titel}' is toegevoegd met ID {boek_id}")

        elif keuze == '2':
            boeken = boek_model.get_all_books()
            print("\nAlle boeken:")
            for boek in boeken:
                print(f"ID: {boek['id']}, Titel: {boek['titel']}, Jaar: {boek['publicatiejaar']}")
                print(f"Plank: {boek['plank_nummer'] or 'Geen'}, Status: {boek['status']}")
                print("-" * 50)

        elif keuze == '3':
            print("Programma wordt afgesloten...")
            print("Programma afgesloten.")
            break
        else:
            print("Ongeldige keuze, probeer het opnieuw.")

    db.close_connection()


if __name__ == "__main__":
    main()