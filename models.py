from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    signature = Column(String, nullable=True)
    cheques = relationship("Cheque", back_populates="person")

class Cheque(Base):
    __tablename__ = "cheques"
    id = Column(Integer, primary_key=True, index=True)
    original_image = Column(String, nullable=False)
    modified_image = Column(String, nullable=True)
    validity = Column(String, nullable=False)
    person_id = Column(Integer, ForeignKey("persons.id"))
    person = relationship("Person", back_populates="cheques")

