"""Database connection and db models"""

from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, Text, String, Boolean
from backend.config import config

engine = create_engine(config.database_engine)
"""Non-autocommit database engine"""

Session = sessionmaker(bind=engine)
"""Uninitialized database session"""

session = Session()
"""Initialized database session"""

Base = declarative_base()
"""Inheritable declarative base"""


class Movies(Base):
    """Movies model"""

    __tablename__ = "movies"
    index = Column(Integer, primary_key=True)
    genre = Column(String(20), nullable=False)
    category = Column(String(15), nullable=False)
    title = Column(String(30), nullable=False)
    year = Column(Integer, nullable=True)
    distribution = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)
    url = Column(String(100), nullable=False)
    cover_photo = Column(String(100), nullable=True)
    is_shown = Column(Boolean, default=True)

    def __repr__(self):
        return f"{self.title} ({self.year})"


def create_all():
    """Create database tables"""
    Base.metadata.create_all(engine)
    session.commit()


def drop_all():
    """Dropd database tables"""
    Base.metadata.drop_all(engine)
    session.commit()
