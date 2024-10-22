from sqlalchemy import create_engine, Column, Integer, Numeric, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class Particulate(Base):
    __tablename__ = 'particulate'
    # Auto-incrementing unique identifier not part of the composite primary key
    instrument_id = Column(Integer, ForeignKey('instrument.id'), primary_key=True, nullable=False)
    date = Column(DateTime, primary_key=True, nullable=False)
    pm1p0_cf1 = Column(Numeric)
    pm2p5_cf1 = Column(Numeric)
    pm10p0_cf1 = Column(Numeric)
    pm1p0_atm = Column(Numeric)
    pm2p5_atm = Column(Numeric)
    pm10p0_atm = Column(Numeric)
    pm0p3_counts = Column(Numeric)
    pm0p5_counts = Column(Numeric)
    pm1p0_counts = Column(Numeric)
    pm2p5_counts = Column(Numeric)
    pm5p0_counts = Column(Numeric)
    pm10p0_counts = Column(Numeric)
    pm_cf1_units = Column(String)
    pm_atm_units = Column(String)
    pm_counts_units = Column(String)
    channel = Column(String, primary_key=True, nullable=False)


if __name__ == "__main__":
    print("Passed")