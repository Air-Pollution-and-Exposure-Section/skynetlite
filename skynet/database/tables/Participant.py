from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from skynet.database.Base import Base
from skynet.database.tables import Emails
from skynet.database.tables import Responsibility

class Participant(Base):
    __tablename__ = 'participant'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    city = Column(String)

    emails = relationship("Emails", back_populates="participant")
    responsibility = relationship("Responsibility", back_populates="participant")


if __name__=="__main__":
    print("Passed")