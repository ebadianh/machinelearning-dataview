import sqlite3
from pathlib import Path
import pandas as pd

CSV_PATH = Path("data/alzheimers_disease_data.csv")
DB_PATH = Path("dementia.db")

def build_database() -> None:
  df = pd.read_csv(CSV_PATH)
  df = df.drop(columns=["DoctorInCharge"])

  conn = sqlite3.connect(DB_PATH)
  df.to_sql("patients", conn, if_exists="replace", index=False)
  conn.close()

if __name__ == "__main__":
  build_database()