from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from typing import Any

class DatabaseManager:
    """
    Centralized database configuration and session management.
    
    Handles database connection, session creation, and provides utility methods.
    """
    
    def __init__(
        self, 
        database_url: str = "postgresql://user:password@localhost/sportsprops",
        echo: bool = False
    ):
        """
        Initialize database engine and session factory.
        
        Args:
            database_url (str): Full database connection string
            echo (bool): Enable SQLAlchemy query logging
        """
        self._engine = create_engine(database_url, echo=echo)
        self._session_factory = sessionmaker(bind=self._engine)
        self._scoped_session = scoped_session(self._session_factory)
    
    @property
    def engine(self):
        """Get database engine."""
        return self._engine
    
    def get_session(self):
        """
        Create and return a new database session.
        
        Returns:
            Session: SQLAlchemy database session
        """
        return self._scoped_session()
    
    def create_all_tables(self):
        """
        Create all database tables based on defined models.
        """
        from .models.user import Base
        Base.metadata.create_all(self._engine)
    
    def drop_all_tables(self):
        """
        Drop all database tables. Use with caution.
        """
        from .models.user import Base
        Base.metadata.drop_all(self._engine)
    
    def transaction(self, func: Any):
        """
        Transaction decorator for database operations.
        
        Ensures atomic database transactions with proper commit/rollback.
        
        Args:
            func (callable): Function to be executed within a transaction
        """
        def wrapper(*args, **kwargs):
            session = self.get_session()
            try:
                result = func(*args, session=session, **kwargs)
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
        return wrapper

# Global database manager instance
db_manager = DatabaseManager()