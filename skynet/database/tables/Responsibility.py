from sqlalchemy import create_engine, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class Responsibility(Base):
    __tablename__ = 'responsibility'
    id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(Integer, ForeignKey('participant.id'))
    instrument_id = Column(Integer, ForeignKey('instrument.id'))
    sample_id = Column(Integer, ForeignKey('sample.id'))
    site_id = Column(Integer, ForeignKey('site.id'))
    location_id = Column(Integer, ForeignKey('location.id'))
    study_id = Column(Integer, ForeignKey('study.id'))
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    # Optional: ORM relationships for easier navigation in Python
    participant = relationship("Participant", back_populates="responsibility")
    instrument = relationship("Instrument", back_populates="responsibility")
    study = relationship("Study", back_populates="responsibility")
    site = relationship("Site", back_populates="responsibility")
    location = relationship("Location", back_populates="responsibility")
