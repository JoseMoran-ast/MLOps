import joblib
import pandas as pd

ARTIFACT_PATH = "rf_forward_model.joblib"

def main():
    artifact = joblib.load(ARTIFACT_PATH)
    model = artifact["model"]
    features = artifact["features"]

    # Ejemplo de delantero (input estático)
    sample = {
        "age": 24,
        "finishing": 82,
        "positioning": 78,
        "shot_power": 80,
        "dribbling": 76,
    }

    X = pd.DataFrame([sample], columns=features)
    pred = float(model.predict(X)[0])

    print("Entrada:", sample)
    print("Prediccion de overall_rating:", pred)

if __name__ == "__main__":
    main()
