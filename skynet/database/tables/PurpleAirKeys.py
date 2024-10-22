from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class PurpleAirKeys(Base):
    __tablename__ = 'purpleair_keys'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Serial type, auto-increments
    instrument_id = Column(Integer, ForeignKey('instrument.id'), nullable=False)
    sensor_id_a = Column(Integer)
    thingspeak_primary_id_a = Column(Integer)
    thingspeak_primary_id_read_key_a = Column(String)
    thingspeak_secondary_id_a = Column(Integer)
    thingspeak_secondary_id_read_key_a = Column(String)
    sensor_id_b = Column(Integer)
    thingspeak_primary_id_b = Column(Integer)
    thingspeak_primary_id_read_key_b = Column(String)
    thingspeak_secondary_id_b = Column(Integer)
    thingspeak_secondary_id_read_key_b = Column(String)

    # Define the ORM relationship for easier navigation
    instrument = relationship("Instrument", back_populates="purpleair_keys")


if __name__ == "__main__":
    print("Passed")