# -*- coding: utf-8 -*-
"""Tester för src/features.py. Kör: python test_features.py

Kollar att featurelistorna stämmer med tabellen i dementia.db.
Bygg databasen först: uv run src/database.py
"""
import pathlib
import sys

from src.data import DB_PATH, load_data
from src.features import FEATURE_SETS, TARGET

# Kolumner som finns i tabellen men aldrig får bli features.
FORBJUDNA = ["PatientID"]

_kolumner = None


def kolumner():
    global _kolumner
    if _kolumner is None:
        if not pathlib.Path(DB_PATH).exists():
            sys.exit(f"{DB_PATH} saknas — kör först: uv run src/database.py")
        _kolumner = set(load_data().columns)
    return _kolumner


def test_alla_features_finns_i_databasen():
    """Ett felstavat kolumnnamn ska falla har, inte langt inne i sklearn."""
    finns = kolumner()
    for namn, features in FEATURE_SETS.items():
        saknas = [f for f in features if f not in finns]
        assert not saknas, f"{namn} har kolumner som inte finns i databasen: {saknas}"


def test_patientid_ar_inte_feature():
    """Korrelationen 0,041 ar en artefakt av radordningen, inte signal."""
    for namn, features in FEATURE_SETS.items():
        for forbjuden in FORBJUDNA:
            assert forbjuden not in features, f"{namn} innehåller {forbjuden}"


def test_targeten_ar_inte_feature():
    """Diagnosis som feature ger nastan 100 % accuracy och betyder ingenting."""
    for namn, features in FEATURE_SETS.items():
        assert TARGET not in features, f"{namn} innehåller targeten {TARGET}"


def test_inga_dubbletter():
    """En kolumn som rakat hamna i tva grupper viktas dubbelt i 'allt'."""
    for namn, features in FEATURE_SETS.items():
        dubbletter = {f for f in features if features.count(f) > 1}
        assert not dubbletter, f"{namn} har dubbletter: {sorted(dubbletter)}"


def test_allt_innehaller_alla_andra_grupper():
    """'allt' ar jamforelsegruppen — saknas en kolumn dar blir jamforelsen skev."""
    allt = set(FEATURE_SETS["allt"])
    for namn, features in FEATURE_SETS.items():
        if namn == "allt":
            continue
        saknas = sorted(set(features) - allt)
        assert not saknas, f"'allt' saknar kolumner från {namn}: {saknas}"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    print("alla tester gick igenom")
