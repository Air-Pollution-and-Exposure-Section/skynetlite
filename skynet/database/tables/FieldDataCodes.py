from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class FieldDataCodes(Base):
    __tablename__ = 'field_data_codes'
    data_code = Column(Integer, primary_key=True)  # data_code as primary key
    source_for_code = Column(Text)  # Use Text for potentially long strings
    sample_status = Column(String, nullable=False)  # Not allowing nulls for sample_status
    explanation = Column(Text)  # Use Text for potentially long explanations

    sample_data = relationship("SampleDataCodes", back_populates="field_data_code")


if __name__ == "__main__":
    print("Passed")