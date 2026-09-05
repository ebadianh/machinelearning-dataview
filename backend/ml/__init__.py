"""ML-lagret för Dataview.

Rena funktioner utan FastAPI-beroenden: modulerna här känner inte till HTTP,
requests eller Pydantic och ska gå att importera och testa fristående.
Preprocessing och modell hålls alltid ihop i ETT sklearn ``Pipeline``-objekt
som sparas med ``joblib``.
"""
