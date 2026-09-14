# -*- coding: utf-8 -*-
"""Semantisk sökning i LOGGBOK.md.

    python logg.py "varför valde vi den modellen"

Indexet byggs om automatiskt när LOGGBOK.md ändrats.
Setup: pip install -r requirements.txt  (första körningen laddar ner modellen, ~220 MB)
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


def entries(text):
    """En loggrad = en chunk. Datumrubriken klistras på så den blir sökbar.
    Överstrukna rader (~~...~~) är ändrade beslut och hoppas över."""
    datum, out = "", []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("## "):
            datum = line[3:].strip()
        elif line and not line.startswith(("#", "~~")):
            out.append(f"{datum} {line}")
    return out


def load(log, cache):
    """Bara nya rader embeddas — annars skulle varje ny loggrad kosta en omindexering
    av hela loggboken, och den kostnaden vaxer for varje dag."""
    rows = entries(log.read_text(encoding="utf-8"))
    cachad = {}
    if cache.exists():
        d = np.load(cache, allow_pickle=True)
        if "modell" in d.files and str(d["modell"]) == MODEL:
            cachad = dict(zip(list(d["rows"]), d["vecs"]))
    nya = [r for r in rows if r not in cachad]
    if nya:
        cachad.update(zip(nya, embed(nya)))
    vecs = np.array([cachad[r] for r in rows]) if rows else np.zeros((0, 1))
    if nya or not cache.exists():
        np.savez(cache, rows=np.array(rows, dtype=object), vecs=vecs, modell=MODEL)
    return rows, vecs


def search(query, k=5, log=LOG, cache=CACHE):
    rows, vecs = load(log, cache)
    if not rows:
        return []
    score = vecs @ embed([query])[0]
    return [(float(score[i]), rows[i]) for i in np.argsort(-score)[:k]]


if __name__ == "__main__":
    # ponytail: Windows-konsolen är cp1252 och loggen är full av åäö och tankstreck
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    arg = " ".join(sys.argv[1:])
    if not arg:
        print(__doc__)
    else:
        for s, row in search(arg):
            print(f"{s:.2f}  {row}")
