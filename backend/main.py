from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
      'http://localhost:3000'
]

app.add_middleware(
      CORSMiddleware,
      allow_origins=origins
)

class SimulationBase(BaseModel):
    input_path: str
    angle_of_attack: float
    output_path: str
    ssim_score: float