from sqlalchemy import create_engine, Column, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class SampleData(Base):
    __tablename__ = 'sample_data'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Serial type, auto-increments
    sample_id = Column(Integer, ForeignKey('sample.id'), nullable=False)
    substance_id = Column(Integer, ForeignKey('substance.id'), nullable=False)
    mass = Column(Numeric)
    lab_detection_limit = Column(Numeric)
    field_detection_limit = Column(Numeric)
    mass_detection_limit = Column(Numeric)
    flag = Column(Numeric)
    concentration_ppb = Column(Numeric)
    concentration_ugm3 = Column(Numeric)
    analytical_method = Column(String)

    # Optional: Define ORM relationships for easier navigation
    sample = relationship("Sample", back_populates="sample_data")
    substance = relationship("Substance", back_populates="sample_data")


if __name__ == "__main__":
    print("Passed")