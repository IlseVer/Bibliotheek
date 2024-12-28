# Bibliotheek
Dit project is een eenvoudig systeem voor het beheren van een thuisbibliotheek. 
Hiermee kun je boeken toevoegen, bijwerken en beheren, evenals de locatie en beschikbaarheid van elk boek bijhouden. 

Het is ontwikkeld in Python en maakt gebruik van een SQLite-database om de gegevens op te slaan.

Indien er geen databasebestand aanwezig is, wordt er automatisch een database aangemaakt die je vervolgens zelf kunt vullen met boeken.

## Inhoud
- [Installatie](#installatie)
  - [Vereisten](#vereisten)
  - [Stappen](#stappen)
- [Functionaliteiten](#functionaliteiten)

## Installatie

### Vereisten
- Python >= 3.8
- Vereiste afhankelijkheden:`requirements.txt`

### Stappen
1. Clone de repository:
   ```bash
   git clone https://github.com/IlseVer/Bibliotheek.git
   ```

2. Maak een virtual environment aan:
   ```bash
   python -m venv .venv
   ```
   Activateer de virtual environment:
   ```bash
   source .venv/bin/activate  # Voor Mac/Linux
   .\.venv\Scripts\Activate.ps1   # Voor Windows Powershell
   .venv\Scripts\activate # Voor Windows cmd
   ```

3. Installeer de benodigde Python-pakketten:
   ```bash
   pip install -r requirements.txt
   ```

4. Plaats het databasebestand 'bibliotheek.db' in de map `database`:
   ```bash
   Bibliotheek/
     ├── database/
     │      ├── 'bibliotheek.db'
     │      ├── ...
     ├── ...
      ```
5. Start het programma:
   ```bash
   python main.py
   
## Functionaliteiten
### 1. Voeg boek toe
- Je kunt een nieuw boek toevoegen aan je bibliotheek door de **titel, publicatiejaar, auteur, genre, locatie** en **beschikbaarheid** in te voeren. 
Dit maakt het makkelijk om je collectie up-to-date te houden.

### 2. Toon alle boeken
- Deze functie toont een **overzicht van alle boeken** die in je bibliotheek zijn opgeslagen.

### 3. Zoek boeken
- op titel
- op genre

### 4. Beheer genres
- **Toevoegen** genres
- **Toon** alle genres
- **Wijzig** een genre

### 5. Wijzig gegevens
 - titel
 - genre
 - locatie
 - beschikbaarheid

### 6. Verwijder boek
### 7. Exporteer boekenlijst naar Excel of csv
- Exporteer de boekenlijst naar een Excel- of csv-bestand die wordt voorzien van een timestamp.

### 8. Statistieken
- aantal boeken per genre
- aantal boeken per publicatiejaar


   


