# Procesamiento de datos
import pandas as pd
import numpy as np
import joblib  #Libreria para crear el artefacto

# Modelado
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

df = pd.read_csv("fifa_players.csv")

# Solo delanteros/extremos
forward_tokens = {"ST", "CF", "LW", "RW"}
df = df[df["positions"].fillna("").apply(
    lambda s: any(pos.strip() in forward_tokens for pos in s.split(","))
)]

# Umbral mínimo de valor
df = df[df["value_euro"] >= 1_000_000]

# Features y target
features = ["age", "finishing", "positioning", "shot_power", "dribbling"]
target = ["overall_rating"]

X = df[features]
y = df[target].to_numpy().ravel()

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Random Forest
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

# Entrenar
model.fit(X_train, y_train)

# Evaluación
pred = model.predict(X_test)
print("R2:", r2_score(y_test, pred))
print("MAE:", mean_absolute_error(y_test, pred))

#Guardo en el artefacto el modelo, las caracteristicas, las posiciones y el coste minimo
artifact = {
    "model": model,
    "features": features,
    "forward_tokens": list(forward_tokens),
    "min_value_euro": 1_000_000
}
joblib.dump(artifact, "rf_forward_model.joblib")
print("Modelo guardado en rf_forward_model.joblib")

# (Opcional) tus cálculos de eficiencia
df["predicted_rating"] = model.predict(X)
df["value_millions"] = df["value_euro"] / 1_000_000
df["efficiency"] = df["predicted_rating"] - 1*np.log1p(df["value_euro"])

top_strikers = df.sort_values("efficiency", ascending=False).head(10)
print("\nTop 10 delanteros más eficientes para comprar:")
print(top_strikers[["name", "positions", "value_euro", "predicted_rating", "efficiency"]])
