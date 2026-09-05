# CLAUDE.md – Dataview

Instruktioner för Claude Code i detta repo. Läs alltid denna fil först.

## Projektet

**Dataview** är en webbapp där användaren laddar upp en CSV, väljer target-kolumn och får
tre tränade och jämförda scikit-learn-modeller.

Stack: **Streamlit** (frontend) → **FastAPI** (backend) → **SQLite + scikit-learn**.

Det är ett skolprojekt med betygsskalan godkänt / icke godkänt. **Enkelhet och att allt
startar från en ren klon väger tyngre än features.** Välj alltid den enklaste lösningen som
fungerar. Tre studenter arbetar i feature-branches mot `main`.

Miljö: Python 3.11+, venv + requirements.txt, Windows med Git Bash.

## Arkitekturprinciper

- **Frontend pratar bara med API:t via HTTP.** Ingen ML-kod, ingen pandas-bearbetning och
  ingen databasåtkomst i Streamlit – bara anrop mot backend och presentation av svaret.
- **All ML ligger i `backend/ml/` som rena funktioner utan FastAPI-beroenden.** Modulerna där
  ska gå att importera och testa fristående; de känner inte till HTTP, requests eller
  Pydantic-modeller.
- **Preprocessing + modell sparas alltid som ETT sklearn `Pipeline`-objekt med `joblib`.**
  Aldrig separata artefakter för encoder/scaler/modell – ett `.joblib` per modell, som
  innehåller hela kedjan från rå DataFrame till prediktion.
- Lagret däremellan (`backend/api/`) gör bara: validera input → anropa `backend/ml/` →
  läsa/skriva i `backend/db/` → returnera Pydantic-svar.

## Konventioner

- Beroenden hanteras med **venv + requirements.txt**. Inga andra pakethanterare.
- Tester skrivs med **pytest** och ligger i `tests/`.
- **Pydantic-scheman för alla request- och response-kroppar**, definierade i `backend/schemas/`.
- **Inga stora datafiler, databaser eller `.joblib`-filer i git.** Uppladdade dataset och
  sparade modeller hamnar i `backend/storage/` som är gitignorerad. Endast det lilla
  syntetiska exempeldatasetet i `data/sample/` får versionshanteras.
- Håll koden liten och läsbar; hellre en tydlig funktion än ett lager abstraktioner.

## Kommandon (Git Bash)

```bash
# Skapa och aktivera venv
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt

# Starta backend (http://127.0.0.1:8000, docs på /docs)
uvicorn backend.main:app --reload

# Starta frontend (i ett andra terminalfönster, med venv aktiverat)
streamlit run frontend/app.py

# Kör tester
pytest

# Generera exempeldata
python data/make_sample.py
```

## Vad som INTE ingår

- Ingen inloggning, inga användarkonton, ingen behörighetshantering.
- Ingen PostgreSQL eller annan databasmotor – bara SQLite.
- Inga bakgrundsjobb, köer eller schemaläggning; träning sker synkront i request.
- Inget annat än **tabulär CSV** – ingen bild, text, tidsserie eller ljud.
- Ingen deployment, Docker eller CI utöver vad som uttryckligen efterfrågas.

## Git

**Kör aldrig git-kommandon i detta projekt.** Inga commits, ingen branch, ingen push,
inget `git add`, inget `git status`. Utvecklarna sköter all versionshantering själva.
Du skapar och redigerar bara filer.
