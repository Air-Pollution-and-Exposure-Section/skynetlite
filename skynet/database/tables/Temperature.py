from sqlalchemy import create_engine, Column, Integer, Numeric, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class Temperature(Base):
    __tablename__ = 'temperature'
    instrument_id = Column(Integer, ForeignKey('instrument.id'), primary_key=True, nullable=False)
    date = Column(DateTime, nullable=False, primary_key=True)  # Part of the composite primary key
    raw_val = Column(Numeric)
    conv_val = Column(Numeric)
    unit = Column(String)


if __name__=="__main__":
    print("Passed")