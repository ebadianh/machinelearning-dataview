import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("dementia.db")

def load_data() -> pd.DataFrame:
  conn = sqlite3.connect(DB_PATH)
  df = pd.read_sql("SELECT * FROM patients", conn)
  conn.close()
  return df