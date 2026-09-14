# -*- coding: utf-8 -*-
"""Tester för logg.py. Kör: python test_logg.py"""
import os
import pathlib
import subprocess
import sys
import tempfile

import numpy as np

import logg

LOGG = """# Loggbok

## 2026-01-02
**Beslut** kör XGBoost istället för logistisk regression — bättre AUC (lukas)

## 2026-01-01
**Beslut** droppar kolumnen Diagnosis från features — läckage (sara)
**Byggt** notebook som plottar ålder mot sjukdomsrisk
"""

NY_RAD = "**Beslut** använder SMOTE mot klassobalans (ali)"


def tmp(text):
    d = pathlib.Path(tempfile.mkdtemp())
    log = d / "LOGGBOK.md"
    log.write_text(text, encoding="utf-8")
    return log, d / "i.npz"


def test_parsning():
    rows = logg.entries(LOGG)
    assert len(rows) == 3, rows
    assert rows[0].startswith("2026-01-02 **Beslut** kör XGBoost"), rows[0]
    assert rows[1].startswith("2026-01-01 **Beslut** droppar"), rows[1]
    assert not any(r.strip().startswith("#") for r in rows), rows


def test_dubbla_datumrubriker():
    """Union-merge kan ge tva '## samma datum' efter varandra."""
    rows = logg.entries("## 2026-01-01\n**Byggt** a\n\n## 2026-01-01\n**Byggt** b\n")
    assert rows == ["2026-01-01 **Byggt** a", "2026-01-01 **Byggt** b"], rows


def test_overstrukna_rader_hoppas_over():
    """Andrat beslut far inte dyka upp som levande i sokresultatet."""
    rows = logg.entries(
        "## 2026-01-01\n"
        "~~**Beslut** kör SVM — bortvalt (lukas)~~ → ändrat 26-01-02\n"
        "**Beslut** kör XGBoost istället — bättre AUC (lukas)\n"
    )
    assert len(rows) == 1, rows
    assert "XGBoost" in rows[0]


def test_tom_loggbok():
    log, cache = tmp("# Loggbok\n")
    assert logg.search("vad som helst", log=log, cache=cache) == []


def test_semantisk_traff_utan_ordlikhet():
    """Fragan innehaller inte ordet XGBoost - det ar hela poangen med embeddings."""
    log, cache = tmp(LOGG)
    hits = logg.search("vilken modell valde vi", log=log, cache=cache)
    assert "XGBoost" in hits[0][1], hits


def test_cache_traffar_nar_filen_ar_orord():
    log, cache = tmp(LOGG)
    first = logg.search("vilken modell valde vi", log=log, cache=cache)
    mtime = cache.stat().st_mtime_ns
    second = logg.search("vilken modell valde vi", log=log, cache=cache)
    assert second == first
    assert cache.stat().st_mtime_ns == mtime, "cachen skrevs om i onodan"


def test_cache_byggs_om_trots_identisk_mtime():
    """Agent skriver rad och soker direkt: mtime kan vara oforandrad, innehallet inte."""
    log, cache = tmp(LOGG)
    logg.search("vilken modell valde vi", log=log, cache=cache)
    stamp = (log.stat().st_atime, log.stat().st_mtime)
    log.write_text(LOGG + "**Beslut** använder SMOTE mot klassobalans (ali)\n", encoding="utf-8")
    os.utime(log, stamp)
    os.utime(cache, stamp)
    hits = logg.search("hur hanterade vi obalans mellan klasserna", log=log, cache=cache)
    assert any("SMOTE" in row for _, row in hits), hits


def test_cli_klarar_windowskonsol():
    """CLAUDE.md sager 'python logg.py <fraga>' - Windows-konsolen ar cp1252,
    som inte kan koda t.ex. pilen i '-> andrat'."""
    import shutil
    d = pathlib.Path(tempfile.mkdtemp())
    shutil.copy(pathlib.Path(__file__).parent / "logg.py", d / "logg.py")
    (d / "LOGGBOK.md").write_text(
        "\n".join(["## 2026-01-01",
                   "**Beslut** kör XGBoost — bättre AUC → vald före SVM (lukas)", ""]),
        encoding="utf-8",
    )
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONIOENCODING", "PYTHONUTF8")}
    p = subprocess.run(
        [sys.executable, "logg.py", "vilken modell valde vi"],
        cwd=d, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    assert p.returncode == 0, p.stderr
    assert "XGBoost" in p.stdout, p.stdout


def test_index_ar_inkrementellt():
    """En ny loggrad far inte kosta omindexering av hela loggboken."""
    log, cache = tmp(LOGG)
    logg.search("vilken modell valde vi", log=log, cache=cache)
    riktig, kallade = logg.embed, []
    logg.embed = lambda t: (kallade.append(list(t)), riktig(t))[1]
    try:
        log.write_text(LOGG + NY_RAD + "\n", encoding="utf-8")
        hits = logg.search("hur hanterade vi obalans mellan klasserna", log=log, cache=cache)
    finally:
        logg.embed = riktig
    indexerade = [t for t in kallade if any("SMOTE" in x for x in t)]
    assert indexerade == [["2026-01-01 " + NY_RAD]], kallade
    assert any("SMOTE" in row for _, row in hits), hits
    assert any("XGBoost" in row for _, row in hits), "gamla rader ska finnas kvar"


def test_modellbyte_bygger_om_indexet():
    """Vektorer fran en annan modell har fel dimension och far inte ateranvandas."""
    log, cache = tmp(LOGG)
    logg.search("vilken modell valde vi", log=log, cache=cache)
    riktig = logg.MODEL
    logg.MODEL = "nagon-annan-modell"
    try:
        rows, vecs = logg.load(log, cache)
        assert len(rows) == len(vecs) == 3, (rows, vecs.shape)
        assert str(np.load(cache, allow_pickle=True)["modell"]) == "nagon-annan-modell"
    finally:
        logg.MODEL = riktig


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    print("alla tester gick igenom")
