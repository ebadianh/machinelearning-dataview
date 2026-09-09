# Loggbok

## 2026-09-09
**Beslut** överstrukna rader indexeras inte — ett ändrat beslut fick annars komma tillbaka som topträff och styra en agent fel — bortvalt: indexera allt och lita på att agenten läser `→ ändrat` (agent/lukas)
**Beslut** cachen jämför sha256 av LOGGBOK.md i stället för mtime — en agent som skriver en rad och söker direkt fick annars gamla träffar — bortvalt: mtime, alltid bygga om (agent/lukas)
**Byggt** `test_logg.py`, 8 tester utan ramverk; tre av dem verifierade att falla när sin fix tas bort
**Problem** cp1252 klarar åäö och tankstreck men inte `→`, så CLI:t kraschade på överstrukna rader — löst med `sys.stdout.reconfigure`
**Beslut** loggboken är en markdownfil i repot med semantisk sökning via `logg.py` — git är redan delat mellan oss tre och kräver ingen drift — bortvalt: riktig databas, vektordatabas, LangChain — (agent/lukas)
**Beslut** embeddings via fastembed + paraphrase-multilingual-MiniLM-L12-v2 — träffade 5/5 testfrågor på svenska mot model2vec 3/5, och kräver inte torch — bortvalt: model2vec, sentence-transformers, embedding-API — (agent/lukas)
**Byggt** `logg.py` med `search` + `selftest`, index cachat i `.logg_index.npz`
