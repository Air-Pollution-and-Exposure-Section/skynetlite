from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class Sample(Base):
    __tablename__ = 'sample'
    id = Column(Integer, primary_key=True)
    eas_sample_id = Column(Text)


if __name__ == "__main__":
    print("Passed")