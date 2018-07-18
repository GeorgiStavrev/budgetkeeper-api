from storage.db import Expenses
from datetime import datetime
from dateutil import parser as date_parser

class ExpensesRepository:
    def __init__(self, db):
        self.db = db

    def get_by_period(self, start, end, limit, offset):
        sess = self.db.get_session()
        query = sess.query(Expenses) \
                    .filter(Expenses.date >= start) \
                    .filter(Expenses.date <= end) \
                    .order_by(Expenses.date) \
                    .limit(limit) \
                    .offset(offset)

        return query.all()
    
    def get_by_id(self, id):
        sess = self.db.get_session()
        return sess.query(Expenses).filter_by(id=id).first()

    def add(self, data):
        sess = self.db.get_session()
        date = date_parser.parse(data['date'])
        expense = Expenses(name=data['name'], date=date, sum=data['sum'])
        sess.add(expense)
        sess.commit()
        sess.close()
    
    def update(self, data, id):
        sess = self.db.get_session()
        expense = sess.query(Expenses).filter_by(id=id).first()
        
        if expense:
            expense.sum = data['sum']
            expense.name = data['name']

        sess.commit()
        sess.close()

        return expense is not None
    
    def delete(self, id):
        sess = self.db.get_session()
        expense = sess.query(Expenses).filter_by(id=id).first()

        if expense:
            sess.delete(expense)

        sess.commit()
        sess.close()

        return expense is not None

    def close(self):
        self.db.close()