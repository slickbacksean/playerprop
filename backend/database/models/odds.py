import uuid
from datetime import datetime
from sqlalchemy import Column, Float, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum as PyEnum

from .user import Base

class OddType(PyEnum):
    MONEYLINE = "moneyline"
    SPREAD = "spread"
    PROP = "prop"
    TOTAL = "total"

class Odds(Base):
    """
    Odds model tracking sports betting odds for various events and prop types.
    
    Captures real-time and historical odds information.
    """
    __tablename__ = 'odds'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    sport = Column(String(50), nullable=False, index=True)
    event = Column(String(100), nullable=False, index=True)
    prop_type = Column(String(50), nullable=False)
    
    odds_type = Column(Enum(OddType), nullable=False)
    
    value = Column(Float, nullable=False)
    implied_probability = Column(Float, nullable=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    event_date = Column(DateTime, nullable=False)
    
    def __repr__(self):
        return f"<Odds {self.prop_type} for {self.event}>"

    def calculate_implied_probability(self) -> float:
        """
        Calculate implied probability from odds value.
        
        Returns:
            float: Implied probability percentage
        """
        if self.value > 0:
            return 100 / (self.value + 100)
        else:
            return abs(self.value) / (abs(self.value) + 100)