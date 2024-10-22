from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Serial type, auto-increments
    name = Column(String, nullable=False)

    # Enforces that the name is unique across all entries in the table
    __table_args__ = (UniqueConstraint('name'),)

    responsibility = relationship("Responsibility", back_populates="site")


if __name__ == '__main__':
    print("Passed")