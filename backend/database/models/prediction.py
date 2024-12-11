import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Float, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum as PyEnum

from .user import Base  # Assuming User model is in the same package

class PredictionStatus(PyEnum):
    PENDING = "pending"
    CORRECT = "correct"
    INCORRECT = "incorrect"
    CANCELLED = "cancelled"

class Prediction(Base):
    """
    Prediction model tracking individual sports prop predictions.
    
    Attributes capture prediction details, associated user, and outcome status.
    """
    __tablename__ = 'predictions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    sport = Column(String(50), nullable=False)
    event = Column(String(100), nullable=False)
    prop_type = Column(String(50), nullable=False)
    
    predicted_value = Column(Float, nullable=False)
    actual_value = Column(Float, nullable=True)
    
    odds = Column(Float, nullable=True)
    potential_winnings = Column(Float, nullable=True)
    
    prediction_date = Column(DateTime, default=datetime.utcnow)
    event_date = Column(DateTime, nullable=False)
    
    status = Column(Enum(PredictionStatus), default=PredictionStatus.PENDING)
    
    # Relationships
    user = relationship("User", back_populates="predictions")
    
    def __repr__(self):
        return f"<Prediction {self.prop_type} for {self.event}>"

    def update_status(self, actual_value: float) -> None:
        """
        Update prediction status based on actual event outcome.
        
        Args:
            actual_value (float): Actual value from the sporting event
        """
        self.actual_value = actual_value
        self.status = (
            PredictionStatus.CORRECT 
            if abs(self.predicted_value - actual_value) < 0.1 
            else PredictionStatus.INCORRECT
        )