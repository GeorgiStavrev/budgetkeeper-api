from sqlalchemy import create_engine, Column, Integer, String, DateTime, REAL, ForeignKey, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import psycopg2

Base = declarative_base()

class StorageProvider:
    def __init__(self, config, verbose=False):
        connString = 'postgres://{}:{}@{}:{}/{}'.format(config['user'], config['password'], config['host'], config['port'], config['database'])
        self.engine = create_engine(connString, echo=verbose)
        self.Session = sessionmaker(bind=self.engine)
    
    def set_up(self):
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        return self.Session()

class Entry(Base):
    __tablename__ = "entries"
    id = Column('id', Integer, primary_key=True)
    kind = Column('kind', Integer)
    name = Column('name', String)
    date = Column('date', DateTime)
    sum = Column('sum', REAL)

    def to_json(self):
        return { 'id': self.id, 'kind': self.kind, 'name': self.name, 'date': self.date.isoformat(), 'sum': self.sum }

class User(Base):
    __tablename__ = "users"
    id = Column('id', Integer, primary_key=True)
    email = Column('email', String)
    hashed_password = Column('hashed_password', String)
    salt = Column('salt', String)

class Budget(Base):
    __tablename__ = "budgets"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    amount = Column('amount', REAL)
    amount_used = Column('amount_used', REAL)