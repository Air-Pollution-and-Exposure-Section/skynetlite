from sqlalchemy import Column, Integer, Numeric, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class Exposure(Base):
    __tablename__ = 'exposure'
    instrument_id = Column(Integer, ForeignKey('instrument.id'), primary_key=True, nullable=False)
    date = Column(DateTime, nullable=False, primary_key=True)  # Part of the composite primary key
    val = Column(Numeric)


if __name__ == "__main__":
    print("Passed")