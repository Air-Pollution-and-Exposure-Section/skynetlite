from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class CO2(Base):
    __tablename__ = 'co2'
    instrument_id = Column(Integer, ForeignKey('instrument.id'), primary_key=True, nullable=False)
    date = Column(DateTime, nullable=False, primary_key=True)  # Part of the composite primary key
    comp_val = Column(Numeric)
    unit = Column(String)


if __name__ == "__main__":
    print("Passed")