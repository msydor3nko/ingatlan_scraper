from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB


Base = declarative_base()


class Apartment(Base):
    """Apartment model class."""

    __tablename__ = "apartments"

    id = Column(Integer, primary_key=True, autoincrement=False)
    url = Column(String(200), nullable=True)
    date_creation = Column(DateTime, default=datetime.utcnow)
    data_artefacts = Column(JSONB, nullable=True)
    address = Column(String(200), nullable=True)
    price = Column(Integer, nullable=True)
    rooms = Column(Integer, nullable=True)
    area = Column(Integer, nullable=True)
    parameters = Column(JSONB, nullable=True)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Apartment: id={self.id} - url={self.url}>"
