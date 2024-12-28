# Bibliotheek
Dit project is een eenvoudig systeem voor het beheren van een thuisbibliotheek. 
Hiermee kun je boeken toevoegen, bijwerken en beheren, evenals de locatie en beschikbaarheid van elk boek bijhouden. 

Het is ontwikkeld in Python en maakt gebruik van een SQLite-database om de gegevens op te slaan.

## Inhoud
- [Installatie](#installatie)
- [Gebruik](#gebruik)
- [Structuur](#structuur)

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
   
## Gebruik

## Structuur
```


