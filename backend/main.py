from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from AeroVision.backend.database import SessionLocal, engine
import models 
import datetime
from fastapi.middleware.cors import CORSMiddleware
import os
os.makedirs("uploads", exist_ok=True)
import numpy as np
import cv2

from .image_processing import preprocess_airfoil
from ml_model.predictor import model_predictor

app = FastAPI()

origins = [
      'http://localhost:3000'
]

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

@app.post("/simulations/", response_model=SimulationModel)
async def submit_simulation(
    db: db_dependency,
    file: UploadFile = File(...),
    angle_of_attack: float = Form(...)
):
    # Save the uploaded file to disk (example)
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Example: You can set output_path and ssim_score as needed
    output_path = "output/path"
    ssim_score = 0.0

    db_simulation = models.Simulation(
        input_path=file_location,
        angle_of_attack=angle_of_attack,
        output_path=output_path,
        ssim_score=ssim_score
    )
    db.add(db_simulation)
    db.commit()
    db.refresh(db_simulation)
    return db_simulation

@app.post("/predict-airflow/",
          tags=["Prediction"],
          summary="Generate Airflow Visualization")
async def predict_airflow_endpoint(
    angle_of_attack: int = Form(...),
    file: UploadFile = File(...)
):
    """
    This endpoint handles the full workflow, now including angle of attack.
    """
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    original_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    processed_input_img = preprocess_airfoil(original_img)
    
    # Pass both the image and the angle to the predictor
    output_visualization_img = model_predictor.predict(
        input_image=processed_input_img,
        angle_of_attack=angle_of_attack
    )

    output_visualization_img_rgb = cv2.cvtColor(output_visualization_img, cv2.COLOR_BGR2RGB)
    success, encoded_img = cv2.imencode(".png", output_visualization_img_rgb)
    
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/png")