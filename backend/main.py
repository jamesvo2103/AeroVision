from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models 
import datetime
from fastapi.middleware.cors import CORSMiddleware

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
async def submit_simulation(simulation: SimulationBase, db: db_dependency):
      db_simulation = models.Simulation(
        input_path=simulation.input_path,
        angle_of_attack=simulation.angle_of_attack,
        output_path=simulation.output_path,
        ssim_score=simulation.ssim_score
      )
      db.add(db_simulation)
      db.commit()
      db.refresh(db_simulation)
      return db_simulation