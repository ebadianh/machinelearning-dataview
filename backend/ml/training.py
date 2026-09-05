"""Träning av de tre modellerna.

Ska för ett dataset och en target:

- dela upp i train/test
- bygga ett ``Pipeline`` per modelltyp: preprocessing från
  ``preprocessing.py`` + estimator (tre olika, t.ex. logistisk regression /
  linjär regression, beslutsträd och random forest)
- träna varje pipeline
- spara varje färdig pipeline som EN ``.joblib``-fil i ``backend/storage/``
  och returnera sökvägen tillsammans med använda feature-namn

Ingen FastAPI-kod här: funktionerna tar DataFrame och kolumnnamn och
returnerar vanliga Python-objekt.
"""
