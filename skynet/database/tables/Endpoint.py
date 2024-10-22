from sqlalchemy import Column, Integer, String
from skynet.database.Base import Base


class Endpoint(Base):
    __tablename__ = 'endpoint'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String)
    description = Column(String)
    url = Column(String)


if __name__ == '__main__':
    print("Proceed")