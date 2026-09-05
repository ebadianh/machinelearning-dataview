"""Genererar ett litet syntetiskt exempeldataset till data/sample/.

Datasetet är tabulärt, har blandade numeriska och kategoriska kolumner, en
binär target (``churn``) och några saknade värden – precis den sortens fil som
Dataview ska kunna ta emot. Använder bara standardbiblioteket så att det går
att köra innan beroendena är installerade.

Kör med:

    python data/make_sample.py
"""

import csv
import random
from pathlib import Path

N_ROWS = 200
SEED = 42
OUTPUT_PATH = Path(__file__).resolve().parent / "sample" / "customers.csv"

CITIES = ["Stockholm", "Göteborg", "Malmö", "Uppsala"]
PLANS = ["basic", "plus", "premium"]
CONTACTED = ["ja", "nej"]

FIELDNAMES = [
    "customer_id",
    "age",
    "monthly_fee",
    "months_active",
    "support_tickets",
    "city",
    "plan",
    "contacted_support",
    "churn",
]


def _maybe_missing(value, probability, rng):
    """Returnerar ett tomt värde med angiven sannolikhet, annars värdet."""
    return "" if rng.random() < probability else value


def make_rows(n_rows=N_ROWS, seed=SEED):
    """Skapar ``n_rows`` rader som dictar, deterministiskt för ett givet seed."""
    rng = random.Random(seed)
    rows = []

    for i in range(1, n_rows + 1):
        age = rng.randint(18, 75)
        plan = rng.choice(PLANS)
        monthly_fee = round({"basic": 99, "plus": 199, "premium": 349}[plan] + rng.gauss(0, 15), 2)
        months_active = rng.randint(1, 60)
        support_tickets = rng.choice([0, 0, 1, 1, 2, 3, 5])
        city = rng.choice(CITIES)
        contacted = rng.choice(CONTACTED)

        # Målvariabeln har ett svagt men verkligt samband med features,
        # så att modellerna har något att lära sig.
        risk = (
            0.5
            + 0.35 * (support_tickets >= 2)
            + 0.25 * (months_active < 12)
            + 0.20 * (plan == "basic")
            - 0.20 * (plan == "premium")
            - 0.01 * (age - 45) / 10
            + rng.gauss(0, 0.35)
        )
        churn = int(risk > 1.0)

        rows.append(
            {
                "customer_id": i,
                "age": _maybe_missing(age, 0.05, rng),
                "monthly_fee": monthly_fee,
                "months_active": months_active,
                "support_tickets": _maybe_missing(support_tickets, 0.04, rng),
                "city": city,
                "plan": _maybe_missing(plan, 0.03, rng),
                "contacted_support": contacted,
                "churn": churn,
            }
        )

    return rows


def main():
    rows = make_rows()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    n_churn = sum(row["churn"] for row in rows)
    print(f"Skrev {len(rows)} rader till {OUTPUT_PATH}")
    print(f"Target 'churn': {n_churn} ettor / {len(rows) - n_churn} nollor")


if __name__ == "__main__":
    main()
