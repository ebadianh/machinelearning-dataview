# Loggbok

## 2026-09-14
**Beslut** nya backlog-kort skrivs onumrerade — numren sitter i issue-titlarna så ett nytt nummer hade tvingat fram omdöpning av hela sekvensen 1–7 — bortvalt: numrera om 1–7, sätta testet som "8." (agent/havash)
**Beslut** testet som låser fast experimentens accuracy-siffror skjuts upp till efter korsvalideringen — siffrorna ändras när #3 landar och ett rött test hade då beskrivit något vi medvetet bytt ut — bortvalt: testa 0,947 och 0,942 nu (agent/havash)
**Beslut** testet byggs på grenen feature/test, inte i main — vi bygger inte i main — bortvalt: commit direkt på main (havash)
**Byggt** test_features.py — 5 tester som vaktar att featurelistorna matchar databasens kolumner och att PatientID och Diagnosis aldrig blir features, alla verifierade att falla när regeln de vaktar bryts (#35)
**Byggt** Done-kolumnen efterregistrerad på board 6 — 10 kort för arbete som redan var gjort (#11, #25–#30, #32–#34)
**Problem** två boards följer samma issues — ebadianh/6 (dataview-kanban) och LukWen-Ill/11 (KK2) — allt nytt ligger bara på 6 och board 11 står kvar med #2–#10 i Todo
**Kvar** smoke-test av README:s körsteg från tom klon — föreslaget, inte upplagt som issue
**Kvar** vem-fältets regel i CLAUDE.md namnger bara lukas — gruppen är tre personer och raderna ovan är skrivna som (agent/havash)
**Beslut** vi arbetar mot en klassisk labbrapport nästlad i uppgiftens fyra obligatoriska rubriker — labbrapportens delar får plats i dem och det är rubrikerna som rättas — bortvalt: ersätta rubrikerna med Syfte/Metod/Resultat/Diskussion (lukas)
**Beslut** hypotes och metod frysas nu medan resultatdelen hålls öppen — vad vi tror och hur vi mätte beror inte på UI-flödet, bara presentationen av resultaten gör det — bortvalt: vänta med hela rapportstrukturen (agent/lukas)
**Kvar** rapportens resultatdel väntar på att UI-flödet i Streamlit-appen är bestämt
**Beslut** rapporten skrivs som markdown i repot under rapport/ — tre personer kan skriva parallellt med vanlig git-hantering och den versionshanteras tillsammans med koden — bortvalt: Word, PDF utanför git (lukas)
**Beslut** rapportens tre första sektioner hämtas ur FINDINGS.md, men utvärderingen av grupparbetet hämtas ur LOGGBOK.md — vem-fältet och Beslut-raderna är enda källan som faktiskt dokumenterar hur gruppen arbetat — bortvalt: skriva grupputvärderingen ur minnet (agent/lukas)
**Kvar** ta reda på om figurer räknas in i rapportens ~3 sidor — frågan går till läraren
**Kvar** fördela rapportens fyra sektioner på gruppens tre personer
**Beslut** merge-konflikten i CLAUDE.md löstes genom att slå ihop båda sidorna — main-versionens projektdokumentation och loggbokreglerna beskriver olika saker och båda behövs — bortvalt: välja en sida (agent/lukas)
**Beslut** CLAUDE.md innehåller hädanefter bara regler — historik hör hemma i loggboken, återstående arbete i GitHub Projects och fynd i FINDINGS.md, och ett dokument som kräver manuell synk varje arbetspass ruttnar — bortvalt: behålla resultat-, att göra- och fyndavsnitten i CLAUDE.md (agent/lukas)
**Beslut** experimentdesignen tränar samma modell på fem featureset mot en baslinje — en enda modell på alla kolumner kan aldrig visa om livsstil bär egen signal — bortvalt: en modell på alla kolumner — importerat från CLAUDE.md, ursprungsdatum okänt (lukas)
**Beslut** databasen är SQLite — publikt repo plus service account-nyckel blir permanent läckage i git-historiken och datan är en platt tabell, inte dokument — bortvalt: Firebase, Firestore, Supabase — importerat från CLAUDE.md, ursprungsdatum okänt (lukas)
**Beslut** genererade artefakter committas inte (*.db, *.joblib) — binärfiler ger olösbara merge-konflikter mellan tre personer och README har körstegen i stället — bortvalt: undantag för dementia.db i .gitignore — importerat från CLAUDE.md, ursprungsdatum okänt (lukas)
**Beslut** Age behålls trots noll-korrelation — att stryka features som inte ger önskat resultat är metodfel och noll-korrelationen är projektets starkaste fynd — bortvalt: droppa Age — importerat från CLAUDE.md, ursprungsdatum okänt (lukas)
**Beslut** EducationLevel räknas som demografi, inte livsstil — utbildningsnivå är strukturellt och inte ett dagligt val — bortvalt: lägga den i livsstil — importerat från CLAUDE.md, ursprungsdatum okänt (lukas)
**Beslut** CSV:n läses exakt en gång, av database.py, all annan kod går via load_data() — en väg in i datan gör att alla kör mot samma tabell — bortvalt: pd.read_csv på flera ställen — importerat från CLAUDE.md, ursprungsdatum okänt (lukas)
**Beslut** PatientID får aldrig bli feature — korrelationen 0,041 är en artefakt av radordningen, inte signal — bortvalt: ta med den som vanlig kolumn — importerat från CLAUDE.md, ursprungsdatum okänt (lukas)
**Beslut** dementia_patients_health_data.csv förkastades till förmån för alzheimers_disease_data.csv — Prescription och Dosage separerar klasserna till 100 % vilket är grovt läckage — bortvalt: dementia_patients_health_data.csv — importerat från CLAUDE.md, ursprungsdatum okänt (lukas)
**Beslut** återstående arbete flyttas till GitHub Projects i stället för en lista i CLAUDE.md — tre personer som redigerar samma lista ger merge-konflikter och boarden visar vem som tagit vad — bortvalt: att göra-lista i CLAUDE.md (agent/lukas)
**Byggt** 9 issues i ebadianh/machinelearning-dataview + board https://github.com/users/LukWen-Ill/projects/11 (publik)

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
