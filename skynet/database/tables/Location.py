from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('name'),)

    responsibility = relationship("Responsibility", back_populates="location")


if __name__ == '__main__':
    print("Passed")