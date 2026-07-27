import os
import io
import datetime
from typing import Annotated

import numpy as np
import cv2
from fastapi import FastAPI, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import SessionLocal, engine
from backend import models
from backend.image_processing import preprocess_airfoil
from ml_model.predictor import model_predictor

os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

app = FastAPI(title="AeroVision API")

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationBase(BaseModel):
    input_path: str
    angle_of_attack: float
    output_path: str
    ssim_score: float


class SimulationModel(SimulationBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)


def _safe_name(filename: str) -> str:
    """Keep only the base name so uploads can't write outside the folder."""
    return os.path.basename(filename or "upload.png")


@app.post("/predict-airflow/",
          tags=["Prediction"],
          summary="Generate Airflow Visualization")
async def predict_airflow_endpoint(
    db: db_dependency,
    angle_of_attack: int = Form(...),
    file: UploadFile = File(...),
):
    """Full workflow: clean the airfoil image, run the model, return a PNG.

    Also logs the run to the database.
    """
    # 1. Read the upload into an image
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    original_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # BGR

    # 2. Save the raw input for the record
    input_path = os.path.join("uploads", _safe_name(file.filename))
    with open(input_path, "wb") as f:
        f.write(contents)

    # 3. Clean/isolate the airfoil shape
    processed_input_img = preprocess_airfoil(original_img)

    # 4. Run the model (returns an RGB image)
    output_rgb = model_predictor.predict(
        input_image=processed_input_img,
        angle_of_attack=angle_of_attack,
    )

    # 5. Save the output and log the run
    output_path = os.path.join("outputs", f"airflow_{_safe_name(file.filename)}.png")
    output_bgr = cv2.cvtColor(output_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, output_bgr)

    db.add(models.Simulation(
        input_path=input_path,
        angle_of_attack=float(angle_of_attack),
        output_path=output_path,
        ssim_score=0.0,
    ))
    db.commit()

    # 6. Stream the PNG back to the browser
    success, encoded_img = cv2.imencode(".png", output_bgr)
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/png")
