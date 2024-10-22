from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from skynet.database.Base import Base


class Substance(Base):
    __tablename__ = 'substance'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Serial type, auto-increments
    name = Column(String)
    iupac = Column(String)
    name_from_lab = Column(String)
    cas_number = Column(String)
    cas_number_no_punctuation = Column(String)
    altname1 = Column(String)
    altname2 = Column(String)
    altname3 = Column(String)
    altname4 = Column(String)
    molecular_weight = Column(Numeric)

    sample_datas = relationship("SampleData", back_populates="substance")


if __name__ == "__main__":
    print("Passed")