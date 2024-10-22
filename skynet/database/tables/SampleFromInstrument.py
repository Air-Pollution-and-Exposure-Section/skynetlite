from sqlalchemy import create_engine, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class SampleFromInstrument(Base):
    __tablename__ = 'sample_from_instrument'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Serial type, auto-increments
    instrument_id = Column(Integer, ForeignKey('instrument.id'), nullable=False)
    sample_id = Column(Integer, ForeignKey('sample.id'), nullable=False)

    # Optional: Define ORM relationships for easier navigation
    instrument = relationship("Instrument", back_populates="sample_from_instrument")
    sample = relationship("Sample", back_populates="sample_from_instrument")


if __name__ == "__main__":
    print("Passed")