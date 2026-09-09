# Loggbok

## 2026-09-09
**Beslut** loggboken är en markdownfil i repot med semantisk sökning via `logg.py` — git är redan delat mellan oss tre och kräver ingen drift — bortvalt: riktig databas, vektordatabas, LangChain — (agent/lukas)
**Beslut** embeddings via fastembed + paraphrase-multilingual-MiniLM-L12-v2 — träffade 5/5 testfrågor på svenska mot model2vec 3/5, och kräver inte torch — bortvalt: model2vec, sentence-transformers, embedding-API — (agent/lukas)
**Byggt** `logg.py` med `search` + `selftest`, index cachat i `.logg_index.npz`
