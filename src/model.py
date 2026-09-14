from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from src.data import load_data
from src.features import FEATURE_SETS, TARGET


# Lambda, inte färdiga objekt: varje körning ska få en NY instans.
# Samma objekt återanvänt över fem featureset skrivs över vid varje fit.
MODELS = {
    "forest": lambda: RandomForestClassifier(random_state=42),
    # SVM mäter avstånd -> måste skalas. StandardScaler ligger INUTI pipen
    # så att fit_transform bara ser träningsdatan (kap 4:9).
    "svm": lambda: make_pipeline(StandardScaler(), SVC(random_state=42)),
}


def run_baseline(df) -> dict:
    X = df[[TARGET]]  # most_frequent läser aldrig X, men split kräver något
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = DummyClassifier(strategy="most_frequent")
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    return {
        "accuracy": accuracy_score(y_test, preds),
        "f1": f1_score(y_test, preds),
    }


def run_experiment(df, feature_names: list[str], model) -> dict:
    """model är nu en parameter — samma mönster som feature_names."""
    X = df[feature_names]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    # cv=5 på HELA datan: skyddar mot att en enskild split råkat bli lätt/svår
    cv_f1 = cross_val_score(model, X, y, cv=5, scoring="f1")

    return {
        "accuracy": accuracy_score(y_test, preds),
        "f1": f1_score(y_test, preds),
        "cv_f1_mean": cv_f1.mean(),
        "cv_f1_std": cv_f1.std(),
    }


def main() -> None:
    df = load_data()

    baseline = run_baseline(df)
    print(f"baslinje             accuracy={baseline['accuracy']:.3f} f1={baseline['f1']:.3f}\n")

    for model_name, make_model in MODELS.items():
        print(f"--- {model_name} ---")
        for name, features in FEATURE_SETS.items():
            r = run_experiment(df, features, make_model())  # ny instans varje varv
            print(
                f"{name:20s} accuracy={r['accuracy']:.3f} f1={r['f1']:.3f} "
                f"cv_f1={r['cv_f1_mean']:.3f} (±{r['cv_f1_std']:.3f})"
            )
        print()


if __name__ == "__main__":
    main()