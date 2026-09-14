# CLAUDE.md — machinelearning-dataview

Den här filen innehåller **bara regler**. Beslutens motiveringar och projektets historik
finns i `LOGGBOK.md`, återstående arbete i GitHub Projects, fynd och siffror i `FINDINGS.md` (byggs — se issue #9).

## Innan du börjar arbeta
1. `git pull`
2. Sök i loggboken efter tidigare beslut som rör uppgiften: `python logg.py "din fråga"`
3. Följ besluten som redan är tagna. Vill du gå emot ett — säg det till användaren först.

## Data
- CSV:n läses exakt en gång, av `src/database.py`. Använd inte `pd.read_csv` någon annanstans — all övrig kod går via `load_data()` i `src/data.py`.
- `PatientID` får aldrig bli feature. Korrelationen är en artefakt av radordningen.
- `DoctorInCharge` droppas vid import i `src/database.py`.
- `Age` behålls trots noll-korrelation. Features stryks inte för att de saknar signal.
- `EducationLevel` hör till demografi, inte livsstil.
- Featureseten definieras i `src/features.py`. Ändra dem där, inte i modellkoden.

## Dataset och databas
- Databasen är SQLite. Firebase och Firestore är avvisade — föreslå dem inte igen.
- `data/alzheimers_disease_data.csv` är projektets dataset.
- `dementia_patients_health_data.csv` är utvärderat och förkastat — föreslå det inte igen.

## Git
- Genererade artefakter committas inte: `*.db`, `*.joblib`. Gör inga undantag för dem i `.gitignore`.

## Köra projektet
```bash
uv sync
uv run src/database.py          # bygger dementia.db
uv run python -m src.model      # kör experimenten
uv run streamlit run app.py     # frontend
```
- Kör modellen som modul (`-m src.model`), aldrig som sökväg. Importerna utgår från projektroten, så sökvägsformen ger `ModuleNotFoundError`.

## Loggbok
Skriv till `LOGGBOK.md`. Nyaste dagen högst upp, rubrik `## ÅÅÅÅ-MM-DD`.
En rad per post, prefix: **Beslut** / **Byggt** / **Problem** / **Kvar**.

- **Beslut** loggas direkt när valet görs, före kod — även val du gör själv utan att fråga.
  Formel: vad — varför (en mening) — bortvalt: x, y — (vem)
- **Byggt** / **Problem** / **Kvar** loggas efter att iterationen funkar.
- Vem-fältet: `(lukas)` för människa, `(agent/lukas)` när en agent bestämde.
- Viktiga agentsamtal loggas som slutsatsen i en Beslut-rad, aldrig som transkript.

Redigera aldrig gamla rader. Ändrat beslut = ny rad idag + stryk den gamla med `~~ ~~` runt hela raden och skriv `→ ändrat ÅÅ-MM-DD`. Överstrukna rader hoppas över av sökningen.

Max en rad per post. Inga rubriker under dagen. Ingen kodstruktur, inga filnamn-listor, inga resonemang. Dagar utan händelse skrivs inte.

## Sökning (RAG)
`logg.py` embeddar varje loggrad och söker semantiskt — du hittar beslut även när du
inte gissar samma ord som skrevs. Indexet (`.logg_index.npz`) är lokalt och byggs om
automatiskt när `LOGGBOK.md` ändrats. Setup en gång: `pip install -r requirements.txt`
(första körningen laddar ner modellen, ~220 MB). Ändrar du `logg.py`: kör `python test_logg.py`.
