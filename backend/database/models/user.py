import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()

class UserRole(PyEnum):
    ADMIN = "admin"
    REGULAR = "regular"
    PREMIUM = "premium"

class User(Base):
    """
    User model representing registered users in the Sports Prop Predictor system.
    
    Attributes cover user authentication, profile, and system interaction details.
    """
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    role = Column(Enum(UserRole), default=UserRole.REGULAR, nullable=False)
    
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    predictions = relationship("Prediction", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}>"

    def is_admin(self) -> bool:
        """Check if user has admin privileges."""
        return self.role == UserRole.ADMIN

    def is_premium(self) -> bool:
        """Check if user has premium access."""
        return self.role == UserRole.PREMIUM