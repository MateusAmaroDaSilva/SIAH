from sqlalchemy import Column, Integer, String, LargeBinary
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    embedding = Column(LargeBinary)  # Salva o embedding como bytes
