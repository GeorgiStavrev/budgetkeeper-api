from sqlalchemy import create_engine, Column, Integer, String, DateTime, REAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import psycopg2
from datetime import datetime
from dateutil import parser as date_parser

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

class Expenses(Base):
    __tablename__ = "expenses"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    date = Column('date', DateTime)
    sum = Column('sum', REAL)

    def to_json(self):
        return { 'id': self.id, 'name': self.name, 'date': self.date.isoformat(), 'sum': self.sum }

class ExpensesRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self, filters=None, limit=None, offset=None):
        sess = self.db.get_session()
        return sess.query(Expenses).all()

    def add(self, data):
        sess = self.db.get_session()
        date = date_parser.parse(data['date'])
        expense = Expenses(name=data['name'], date=date, sum=data['sum'])
        sess.add(expense)
        sess.commit()
        sess.close()