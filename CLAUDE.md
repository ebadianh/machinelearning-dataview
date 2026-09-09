# CLAUDE.md

## Projektet
Vi är tre som tränar modeller på ett Kaggle-dataset om Alzheimers. Frågan vi undersöker:
går det att utifrån livsstilsfaktorer prediktera vem som riskerar att utveckla Alzheimers?

## Innan du börjar arbeta
1. `git pull`
2. Sök i loggboken efter tidigare beslut som rör uppgiften: `python logg.py "din fråga"`
3. Följ besluten som redan är tagna. Vill du gå emot ett — säg det till användaren först.

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
