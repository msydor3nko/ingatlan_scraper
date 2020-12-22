# from sqlalchemy import Column, Integer, String, Text, Float, CHAR, DECIMAL, create_engine
from sqlalchemy import create_engine, Column, String, Text, BigInteger, CHAR, DECIMAL, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime
from config import POSTGRES_DATABASE


Base = declarative_base()

class ApartDB(Base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    _id = "apart_id"
    url = Column(String(1000), nullable=True)
    address = Column(String(500), nullable=True)
    price = Column(DECIMAL(precision=6, scale=2))
    rooms = Column(Integer, nullable=True)
    area = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    date_creation = DateTime(default=datetime.utcnow)
    parameters = Column(Text, nullable=True)    # JSON

    def __init__(self):
        # database connection settings
        db_connect = POSTGRES_DATABASE or 'sqlite:///memory.db'
        # setup database session
        engine = create_engine(db_connect, echo=True)
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        # init database session
        session = Session()

    def __repr__(self):
        return f"<Apart: id={self.id} - url={self.url}>"
    
    def save_to_db(self, **kwargs):
        try:
            apart = Apart(
                url=kwargs.get('url'),
                address=kwargs.get('address'),
                # ...
            )
            self.session.add(apart)
            self.session.commit()
            print(f'Saved: {kwargs}')

        except Exception as exc:
            print(f"ScraperBase exception: {exc}")

        finally:
            self.session.close()
            print('ScraperBase session closed.')


### Check saved data in SQLite using console commands ###

# open database
# sqlite3 memory.db

# show tables
# sqlite> .tables

# show content in 'products'table
# sqlite> .headers ON
# sqlite> .mode column
# sqlite> SELECT * FROM products;
