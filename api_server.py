import joblib
import pandas as pd
import os 

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

ARTIFACT_PATH = os.getenv(
    "MODEL_PATH",
    "/opt/mlops/artifacts/rf_forward_model.joblib"
)

if not os.path.exists(ARTIFACT_PATH):
    raise FileNotFoundError(
        f"Model file not found at {ARTIFACT_PATH}"
    )

# Cargar artefacto al arrancar
artifact = joblib.load(ARTIFACT_PATH)
model = artifact["model"]
features = artifact["features"]

app = FastAPI(title="Forward Scouting API", version="1.0")

templates = Jinja2Templates(directory="templates")


class InferRequest(BaseModel):
    age: float = Field(..., ge=0, le=60)
    finishing: float = Field(..., ge=0, le=100)
    positioning: float = Field(..., ge=0, le=100)
    shot_power: float = Field(..., ge=0, le=100)
    dribbling: float = Field(..., ge=0, le=100)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Renderiza la interfaz web
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/infer")
def infer(req: InferRequest):
    row = req.model_dump()
    X = pd.DataFrame([row], columns=features)
    pred = float(model.predict(X)[0])
    return {"predicted_overall_rating": pred}
