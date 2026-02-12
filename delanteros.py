#Procesamiento de datos
import pandas as pd
import numpy as np

#Modelado
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

df = pd.read_csv("fifa_players.csv")
#Solo quiero jugadores que sean delanteros o extremos
forward_tokens = {"ST", "CF", "LW", "RW"}

df = df[df["positions"].fillna("").apply(
    lambda s: any(pos.strip() in forward_tokens for pos in s.split(","))
)]
#Para que no de fallo en algún calculo elimino los jugadores que no tengan valor
df = df[df["value_euro"] >= 1_000_000]
#Hay que dividir los datos en features (X) y target (Y)
features = ["age", "finishing", "positioning", "shot_power", "dribbling"]
target = ["overall_rating"]
X = df[features]
y = df[target].to_numpy().ravel()

#Lo siguiente es dividir los datos en training y test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Ahora creao el random forest
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)
#Lo entreno
model.fit(X_train, y_train)

# Se hace la evaluacion
pred = model.predict(X_test)

print("R2:", r2_score(y_test, pred))
print("MAE:", mean_absolute_error(y_test, pred))

#Calcular eficiencia de compra
df["predicted_rating"] = model.predict(X)

df["value_millions"] = df["value_euro"] / 1_000_000
df["efficiency"] = df["predicted_rating"] - 1*np.log1p(df["value_euro"])


# Creo un top 10 de los resultados
top_strikers = df.sort_values("efficiency", ascending=False).head(10)

print("\nTop 10 delanteros más eficientes para comprar:")
print(top_strikers[["name", "positions", "value_euro", "predicted_rating", "efficiency"]])
