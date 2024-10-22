from sqlalchemy import create_engine, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from skynet.database.Base import Base

class Emails(Base):
  __tablename__ = 'emails'
  id = Column(Integer, primary_key=True, autoincrement=True)
  participant_id = Column(Integer, ForeignKey('participant.id'))
  email = Column(String)

  participant = relationship("Participant", back_populates="emails")
