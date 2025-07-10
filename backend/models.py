from AeroVision.backend.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
class Simulation(Base):
      __tablename__ = 'simulations'
      
      id = Column(Integer, primary_key=True, index=True)
      input_path      = Column(String,  nullable=False)
      angle_of_attack = Column(Float,   nullable=False)
      output_path     = Column(String,  nullable=False)
      ssim_score      = Column(Float)
      created_at      = Column(DateTime, default=datetime.utcnow)
