"""Preprocessing som en del av sklearn-pipelinen.

Ska bygga en ``ColumnTransformer`` som hanterar rå data direkt från CSV:n:

- numeriska kolumner: imputering av saknade värden + skalning
- kategoriska kolumner: imputering + one-hot-encoding med
  ``handle_unknown="ignore"``

Funktionerna här returnerar transformer-objekt, inte transformerad data.
Transformern sätts ihop med modellen till ett enda ``Pipeline`` i
``training.py`` så att samma steg alltid följer med vid prediktion.
"""
