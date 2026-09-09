# Loggbok

## 2026-09-09
**Beslut** stannar på MiniLM-modellen — en sökning tar 3,2 s mot mpnets 5,7 s och latens väger tyngre än träffkvalitet här — bortvalt: mpnet (7/8 mot 5/8 rätt i topp-3, men +2,5 s per sökning) (agent/lukas)
**Beslut** indexet uppdateras inkrementellt, bara nya rader embeddas — full omindexering kostade 37 s vid 500 rader och skulle utlösas av varje ny loggrad — bortvalt: full omindexering, daemon som håller modellen varm (agent/lukas)
**Beslut** datum och prefix skickas med till modellen — mätning visar att prefixet höjer träffsäkerheten (6/8 mot 4/8) och datumet inte stör mätbart, dessutom går det då att söka på datum — bortvalt: skicka bara innehållet (agent/lukas)
**Byggt** inkrementell indexering + modellnamn i cachen, 10 tester totalt
**Problem** författare och skrivstil påverkar inte sökningen (0,96 för samma innehåll av olika personer mot 0,36 för olika innehåll av samma person)
**Beslut** överstrukna rader indexeras inte — ett ändrat beslut fick annars komma tillbaka som topträff och styra en agent fel — bortvalt: indexera allt och lita på att agenten läser `→ ändrat` (agent/lukas)
**Beslut** cachen jämför sha256 av LOGGBOK.md i stället för mtime — en agent som skriver en rad och söker direkt fick annars gamla träffar — bortvalt: mtime, alltid bygga om (agent/lukas)
**Byggt** `test_logg.py`, 8 tester utan ramverk; tre av dem verifierade att falla när sin fix tas bort
**Problem** cp1252 klarar åäö och tankstreck men inte `→`, så CLI:t kraschade på överstrukna rader — löst med `sys.stdout.reconfigure`
**Beslut** loggboken är en markdownfil i repot med semantisk sökning via `logg.py` — git är redan delat mellan oss tre och kräver ingen drift — bortvalt: riktig databas, vektordatabas, LangChain — (agent/lukas)
**Beslut** embeddings via fastembed + paraphrase-multilingual-MiniLM-L12-v2 — träffade 5/5 testfrågor på svenska mot model2vec 3/5, och kräver inte torch — bortvalt: model2vec, sentence-transformers, embedding-API — (agent/lukas)
**Byggt** `logg.py` med `search` + `selftest`, index cachat i `.logg_index.npz`
