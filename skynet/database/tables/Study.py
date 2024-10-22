from sqlalchemy import Column, Integer, DateTime, Text, Sequence
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class Study(Base):
    __tablename__ = 'study'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    contact = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    city = Column(Text)
    state_province = Column(Text)
    county = Column(Text)
    country = Column(Text)
    long_name = Column(Text)
    description = Column(Text)

    responsibility = relationship("Responsibility", back_populates="study")


if __name__ == '__main__':
    print("Passed")