from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, Text
from sqlalchemy.dialects.postgresql import INET
from skynet.database.Base import Base
from sqlalchemy.orm import relationship

from skynet.database.tables.Responsibility import Responsibility
from skynet.database.tables.Participant import Participant
from skynet.database.tables.Study import Study
from skynet.database.tables.Site import Site
from skynet.database.tables.Location import Location



class Instrument(Base):
    __tablename__ = 'instrument'
    id = Column(Integer, primary_key=True, autoincrement=True)
    manufacturer = Column(String)
    name = Column(String)
    model = Column(String)
    type = Column(String)
    serial_number = Column(String)
    mac_address = Column(String)
    software_version = Column(String)
    owner_email = Column(String)
    associated_email = Column(String)
    label = Column(String)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    device_location_type = Column(String)
    online = Column(Boolean)
    ip_address = Column(INET)
    wifi_password = Column(String)
    sim_number = Column(Numeric)
    phone_number = Column(Numeric)
    imei_number = Column(Numeric)
    comments = Column(Text)

    purpleair_keys = relationship("PurpleAirKeys", back_populates="instrument")
    responsibility = relationship("Responsibility", back_populates="instrument")


if __name__ == "__main__":
    print("Passed")
