# -*- coding: utf-8 -*-
"""Semantisk sökning i LOGGBOK.md.

    python logg.py "varför valde vi den modellen"
    python logg.py selftest

Indexet byggs om automatiskt när LOGGBOK.md ändrats. Kräver: pip install -r requirements.txt
"""
import pathlib
import sys

import numpy as np
from fastembed import TextEmbedding

ROOT = pathlib.Path(__file__).parent
LOG = ROOT / "LOGGBOK.md"
CACHE = ROOT / ".logg_index.npz"
MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

_model = None


def embed(texts):
    global _model
    if _model is None:
        _model = TextEmbedding(MODEL)
    v = np.array(list(_model.embed(texts)))
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def entries(path):
    """En loggrad = en chunk. Datumrubriken klistras på så den blir sökbar."""
    datum, out = "", []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("## "):
            datum = line[3:].strip()
        elif line and not line.startswith("#"):
            out.append(f"{datum} {line}")
    return out


def load(log, cache):
    if cache.exists() and cache.stat().st_mtime >= log.stat().st_mtime:
        d = np.load(cache, allow_pickle=True)
        return list(d["rows"]), d["vecs"]
    rows = entries(log)
    vecs = embed(rows) if rows else np.zeros((0, 1))
    np.savez(cache, rows=np.array(rows, dtype=object), vecs=vecs)
    return rows, vecs


def search(query, k=5, log=LOG, cache=CACHE):
    rows, vecs = load(log, cache)
    if not rows:
        return []
    score = vecs @ embed([query])[0]
    return [(float(score[i]), rows[i]) for i in np.argsort(-score)[:k]]


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        log, cache = pathlib.Path(d) / "L.md", pathlib.Path(d) / "i.npz"
        log.write_text(
            "## 2026-01-01\n"
            "**Beslut** kör XGBoost istället för logistisk regression — bättre AUC (lukas)\n"
            "**Beslut** droppar kolumnen Diagnosis från features — läckage (sara)\n"
            "**Byggt** notebook som plottar ålder mot sjukdomsrisk\n",
            encoding="utf-8",
        )
        hits = search("vilken modell valde vi", log=log, cache=cache)
        assert "XGBoost" in hits[0][1], hits
        assert cache.exists()
        assert search("vilken modell valde vi", log=log, cache=cache)[0][1] == hits[0][1]
    print("selftest ok")


if __name__ == "__main__":
    arg = " ".join(sys.argv[1:])
    if arg == "selftest":
        selftest()
    elif arg:
        for s, row in search(arg):
            print(f"{s:.2f}  {row}")
    else:
        print(__doc__)
