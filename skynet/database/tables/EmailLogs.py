from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from skynet.database.Base import Base

class EmailLogs(Base):
    __tablename__ = 'email_logs'

    date = Column(DateTime, nullable=False, primary_key=True)  # Part of the composite primary key
    participant_id = Column(Integer, ForeignKey('participant.id'), primary_key=True)
    status_code = Column(Integer)
    error = Column(String)
    message = Column(String)