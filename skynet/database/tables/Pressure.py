from sqlalchemy import create_engine, Column, Integer, Numeric, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class Pressure(Base):
    __tablename__ = 'pressure'
    # No need for autoincrement=True since 'id' is a serial type, which automatically increments
    instrument_id = Column(Integer, ForeignKey('instrument.id'), primary_key=True, nullable=False)
    date = Column(DateTime, nullable=False, primary_key=True)  # Part of the composite primary key
    val = Column(Numeric)
    unit = Column(String)
    

if __name__ == "__main__":
    print("Passed")