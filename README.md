# Dataview

Ladda upp en CSV, välj target-kolumn och få tre tränade och jämförda scikit-learn-modeller.

Stack: Streamlit (frontend) → FastAPI (backend) → SQLite + scikit-learn.

## Kom igång

Kräver Python 3.11 eller senare. Kommandona nedan är för Git Bash på Windows.

```bash
# 1. Klona och gå in i mappen
git clone https://github.com/ebadianh/machinelearning-dataview.git
cd machinelearning-dataview

# 2. Skapa och aktivera en virtuell miljö
python -m venv venv
source venv/Scripts/activate

# 3. Installera beroenden
pip install -r requirements.txt
```

## Starta appen

Backend och frontend körs i varsitt terminalfönster, båda med venv aktiverat.

```bash
# Terminal 1 – backend på http://127.0.0.1:8000 (API-dokumentation på /docs)
uvicorn backend.main:app --reload

# Terminal 2 – frontend på http://localhost:8501
streamlit run frontend/app.py
```

## Tester

```bash
pytest
```

## Exempeldata

Ett litet syntetiskt dataset ligger i `data/sample/customers.csv`. Det kan genereras om med:

```bash
python data/make_sample.py
```

## Projektstruktur

```
backend/
  main.py        FastAPI-appen
  api/           HTTP-routers
  schemas/       Pydantic-scheman
  db/            SQLite (tabellerna datasets, runs, models)
  ml/            Profilering, validering, preprocessing, träning, utvärdering
  storage/       Uppladdade filer, databas och sparade modeller (ej i git)
frontend/
  app.py         Streamlit-gränssnittet
data/
  make_sample.py Genererar exempeldata
tests/           pytest
```
