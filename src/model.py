from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

from src.data import load_data
from src.features import FEATURE_SETS, TARGET

def run_baseline(df) -> dict:
  X = df[[TARGET]]
  y = df[TARGET]
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

  model = DummyClassifier(strategy="most_frequent")
  model.fit(X_train, y_train)
  preds = model.predict(X_test)

  return {
        "accuracy": accuracy_score(y_test, preds),
        "f1": f1_score(y_test, preds),
    }

def run_experiment(df, feature_names: list[str]) -> dict:
  X = df[feature_names]
  y = df[TARGET]

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

  model = RandomForestClassifier(random_state=42)
  model.fit(X_train, y_train)
  preds = model.predict(X_test)

  return {
        "accuracy": accuracy_score(y_test, preds),
        "f1": f1_score(y_test, preds),
    }


def main() -> None:
    df = load_data()

    baseline = run_baseline(df)
    print(f"{'baslinje':20s} accuracy={baseline['accuracy']:.3f} f1={baseline['f1']:.3f}")

    for name, features in FEATURE_SETS.items():
        result = run_experiment(df, features)
        print(f"{name:20s} accuracy={result['accuracy']:.3f} f1={result['f1']:.3f}")

if __name__ == "__main__":
    main()
