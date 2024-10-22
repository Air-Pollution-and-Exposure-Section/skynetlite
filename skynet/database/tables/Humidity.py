from sqlalchemy import create_engine, Column, Integer, Numeric, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class Humidity(Base):
    __tablename__ = 'humidity'
    instrument_id = Column(Integer, ForeignKey('instrument.id'), primary_key=True, nullable=False)
    date = Column(DateTime, primary_key=True, nullable=False)
    raw_val = Column(Numeric)
    conv_val = Column(Numeric)
    unit = Column(String)


if __name__ == "__main__":
    print("Passed")