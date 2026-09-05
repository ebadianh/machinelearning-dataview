"""Profilering av ett uppladdat dataset.

Ska ta en pandas DataFrame och beskriva den så att frontend kan visa en
översikt och användaren kan välja target-kolumn:

- antal rader och kolumner
- per kolumn: dtype, antal saknade värden, antal unika värden
- om kolumnen ska behandlas som numerisk eller kategorisk
- enkel beskrivande statistik (min/median/max för numeriska, topp-kategorier
  för kategoriska)

Resultatet är en vanlig dict som kan sparas som JSON i ``datasets.profile_json``.
"""
