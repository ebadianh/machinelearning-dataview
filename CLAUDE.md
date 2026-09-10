# CLAUDE.md — machinelearning-dataview

> Läs hela den här filen innan du föreslår något. Den innehåller beslut som redan är fattade och motiverade. Föreslå inte om något som står under "Beslut" utan att först fråga.

---

## 1. Vad projektet är

Kunskapskontroll del 2, kursen **AI – teori och tillämpning del 1**, klass MAI24MA, NBI/Handelsakademin. Grupparbete, 3 personer.

**Krav från uppgiften:**

1. Data ska lagras i en databas / backend
2. AI-modellering i Python
3. Frontend i Streamlit
4. Git/GitHub obligatoriskt — publikt repo med README
5. Teknisk rapport ~3 sidor: bakgrund, huvudresultat, teknisk specifikation, utvärdering av grupparbetet

**Redovisning:** kursvecka 6 = v.39 (börjar måndag 21 september 2026).

**Repo:** `git@github.com:ebadianh/machinelearning-dataview.git` (publikt)

---

## 2. Frågeställning

**Bär livsstilsfaktorer signal för Alzheimerdiagnos i det här datasetet, jämfört med kliniska bedömningar?**

Experimentdesignen svarar på frågan genom att träna **samma modell på fem olika featureset** och jämföra mot en baslinje. Om livsstilsmodellen landar på baslinjen är *det* svaret. En enda modell tränad på alla kolumner kan aldrig visa det.

---

## 3. Dataset

`data/alzheimers_disease_data.csv` — 2149 rader × 35 kolumner.

**Target:** `Diagnosis` — 1389 nollor / 760 ettor (35,4 % positiva).
**Baslinje (majoritetsgissning):** 64,6 %.

### Viktiga fynd i datan

| Fynd | Detalj |
|---|---|
| Livsstil bär ingen signal | Smoking −0,005, AlcoholConsumption −0,008, PhysicalActivity 0,006, DietQuality 0,009, SleepQuality −0,057, BMI 0,026 — alla inom ±0,06 mot target |
| **Ålder bär ingen signal** | Korrelation −0,0055. Andel diagnos per åldersgrupp: 60–64: 38,2 %, 65–69: 33,2 %, 70–74: 33,9 %, 75–79: 35,8 %, 80–84: 35,5 %, 85–90: 35,6 %. Platt linje. |
| All signal sitter i kliniska bedömningar | FunctionalAssessment −0,37, ADL −0,33, MemoryComplaints 0,31, MMSE −0,24 |
| `DoctorInCharge` | Ett enda värde ("XXXConfid") → droppas vid import i `database.py` |
| `PatientID` | Korrelation 0,041, artefakt av radordning → får **aldrig** bli feature |

**MMSE** = Mini-Mental State Examination (0–30, under 24 indikerar nedsättning).
**ADL** = Activities of Daily Living (självständighet i vardagen).
Båda bedöms av vårdpersonal — de mäter *symtom*, inte orsaker.

### Detta är projektets centrala poäng

Ålder är den starkaste kända riskfaktorn för Alzheimer i verkligheten. Att den är helt platt här **bevisar att datan är syntetisk** — bara de kliniska bedömningarna har kopplats till diagnosen.

Slutsatsen i rapporten får därför **inte** bli "livsstil påverkar inte demens". Den ska bli: *i det här datasetet bär varken livsstil eller ålder signal, vilket tyder på syntetiskt genererad data.* Åldersplotten ska med i rapporten som belägg.

---

## 4. Beslut (ifrågasätt inte utan att fråga)

**SQLite, inte Firebase/Supabase.** Publikt repo + service account-nyckel = permanent läckage i git-historiken. Läraren saknar credentials vid klon. Firestore är NoSQL medan datan är en platt tabell. SQLite är en fullvärdig relationsdatabas — SQL, primärnycklar, transaktioner. *Firebase är definitivt avvisat.* Postgres via Supabase/Neon kan bli en bonus senare, men då sätter vi upp credentials själva.

**Genererade artefakter committas inte** (`*.db`, `*.joblib`). Binärfiler ger olösbara merge-konflikter mellan tre personer. README har körstegen i stället — reproducerbarhet ser dessutom starkare ut i ett CV-repo. Gör inte `!dementia.db`-undantag i .gitignore.

**Age behålls trots noll-korrelation.** Att stryka features som inte ger önskat resultat är metodfel. Noll-korrelationen är projektets starkaste fynd.

**EducationLevel ligger i DEMOGRAPHICS, inte LIFESTYLE.** Utbildningsnivå är strukturellt, inte ett dagligt val. Ska motiveras i rapporten.

**CSV läses exakt en gång**, av `database.py`. All annan kod går via `data.load_data()` som läser från SQLite. Använd inte `pd.read_csv` någon annanstans.

---

## 5. Struktur

```
data/alzheimers_disease_data.csv
src/database.py      CSV → SQLite. Droppar DoctorInCharge.
src/data.py          load_data() → SELECT * FROM patients → DataFrame
src/features.py      Featurelistor + FEATURE_SETS + TARGET
src/model.py         run_baseline, run_experiment, main
app.py               Streamlit (ej byggd än)
README.md
dementia.db          genererad, gitignorerad
```

### Featureset i `features.py`

| Nyckel | Innehåll | Antal |
|---|---|---|
| `demografi` | Age, Gender, Ethnicity, EducationLevel | 4 |
| `livsstil` | BMI, Smoking, AlcoholConsumption, PhysicalActivity, DietQuality, SleepQuality | 6 |
| `sjukdomshistorik` | FamilyHistoryAlzheimers, CardiovascularDisease, Diabetes, Depression, HeadInjury, Hypertension | 6 |
| `kliniskt` | MMSE, FunctionalAssessment, ADL, MemoryComplaints, BehavioralProblems, Confusion, Disorientation, PersonalityChanges, DifficultyCompletingTasks, Forgetfulness | 10 |
| `allt` | Alla ovan + VITALS (blodtryck, kolesterol) | 32 |

`TARGET = "Diagnosis"`

---

## 6. Köra projektet

```bash
uv sync
uv run src/database.py          # bygger dementia.db
uv run python -m src.model      # kör experimenten
uv run streamlit run app.py     # frontend
```

**Obs `-m src.model`, inte `src/model.py`.** Importerna är `from src.data import ...`, alltså adresser som utgår från projektroten. Kör du filen som sökväg ställer sig Python inne i `src/` och hittar ingen mapp som heter `src` → `ModuleNotFoundError`.

**Beroenden** (`pyproject.toml`): matplotlib>=3.11.1, pandas>=3.0.5, scikit-learn>=1.9.0, streamlit>=1.63.0. Dev: ipykernel>=7.3.0, jupyter>=1.1.1. `uv.lock` är committad.

Paketet heter `scikit-learn` vid installation, `sklearn` vid import. Får du "could not be resolved from source" i VS Code är det Pylance som pekar fel: Cmd+Shift+P → Python: Select Interpreter → `.venv/bin/python`.

---

## 7. Resultat hittills

```
baslinje             accuracy=0.647  f1=0.000
demografi            accuracy=0.551  f1=0.313
livsstil             accuracy=0.602  f1=0.114
sjukdomshistorik     accuracy=0.635  f1=0.048
kliniskt             accuracy=0.947  f1=0.924
allt                 accuracy=0.942  f1=0.915
```

Modell: `RandomForestClassifier(random_state=42)`. Split: `test_size=0.2, random_state=42, stratify=y` — identisk i alla körningar, därför räcker **en** baslinjerad för alla fem.

### Så här ska siffrorna läsas

- **Tre modeller ligger under baslinjen.** Demografi, livsstil och sjukdomshistorik slår inte "gissa alltid noll".
- **Låg F1 vid hyfsad accuracy = modellen säger nästan aldrig "demens".** Sjukdomshistorik: accuracy 0,635 ser ut som "63 % rätt", men F1 0,048 avslöjar att den i praktiken gissar nollan.
- **Baslinjens F1 är exakt 0,000** — den predikterar aldrig den positiva klassen.
- **`kliniskt` (0,947) slår `allt` (0,942)** med 10 features mot 32. Random Forest väljer slumpmässigt features vid varje split; med 22 brusiga kolumner i mängden hamnar den ibland i lägen där bara brus finns att dela på.
- **Men:** skillnaden 0,947 vs 0,942 kommer från *en* split. Innan något skrivs om den i rapporten måste den verifieras med korsvalidering.

---

## 8. Att göra

**Nästa steg, i ordning:**

1. **Korsvalidering** — verifiera att skillnaden kliniskt/allt inte är slump från en enskild split
2. **Spara tränad modell med joblib** — Streamlit-appen får inte träna om vid varje sidladdning
3. **Bygg `app.py`** (Streamlit)
4. **README** med de fyra körstegen — testa i en färsk klon före inlämning
5. **Teknisk rapport** ~3 sidor
6. Töm/radera `main.py` (innehåller `uv init`-rester)
7. Committa uv.lock-ändringar

**Gruppen behöver bestämma:**

- Flöde för merge-konflikter i notebooks
- Om `dev` är integrationsgren eller inte
- Vad `backend/storage/` i .gitignore refererar till (oklart, aldrig utrett)

**Del 1** (individuell, glöm inte): övningsuppgifter kap 1–6 som **exekverade** Jupyter notebooks.

---

## 9. Avvisat dataset — ta inte upp igen

**`dementia_patients_health_data.csv`** (1000 rader) utvärderades och förkastades:

- `Prescription` och `Dosage in mg` är NaN för exakt alla 515 friska och ifyllda för alla 485 dementa → 100 % separation, grovt läckage
- `Depression_Status = Yes` → 100 % dementa
- `Cognitive_Test_Scores` korrelation −0,843
- Livsstilsvariabler på slumpnivå (~0,50); nuvarande rökare hade 0,00 demens = biologiskt orimligt
- APOE_ε4 (0,16 vs 0,63) var enda reella signal

Därför valdes `alzheimers_disease_data.csv` i stället.

---

*Uppdatera avsnitt 7 och 8 efter varje arbetspass.*
