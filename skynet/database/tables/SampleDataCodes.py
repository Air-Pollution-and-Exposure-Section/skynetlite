from sqlalchemy import create_engine, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class SampleDataCodes(Base):
    __tablename__ = 'sample_data_codes'
    id = Column(Integer, primary_key=True)  # Serial type, auto-increments
    sample_id = Column(Integer, ForeignKey('sample.id'), nullable=False)
    data_code = Column(Integer, ForeignKey('field_data_codes.data_code'), nullable=False)

    # Optional: Define ORM relationships for easier navigation
    sample = relationship("Sample", back_populates="sample_data_codes")
    field_data_code = relationship("FieldDataCodes", back_populates="sample_data_codes")


if __name__ == "__main__":
    print("Passed")