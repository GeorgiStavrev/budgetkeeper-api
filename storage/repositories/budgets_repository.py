from storage.db import Budget

class BudgetsRepository:
    def __init__(self, db):
        self.db = db
        
    def get_by_id(self, id):
        sess = self.db.get_session()
        return sess.query(Budget).filter_by(id=id).first()

    def add(self, data):
        sess = self.db.get_session()
        budget = Budget(name=data['name'], sum=data['amount'])
        sess.add(budget)
        sess.commit()
        sess.close()
    
    def update(self, data, id):
        sess = self.db.get_session()
        budget = sess.query(Budget).filter_by(id=id).first()
        
        if budget:
            budget.sum = data['sum']
            budget.amount = data['amount']

        sess.commit()
        sess.close()

        return budget is not None
    
    def delete(self, id):
        sess = self.db.get_session()
        budget = sess.query(Budget).filter_by(id=id).first()

        if budget:
            sess.delete(budget)

        sess.commit()
        sess.close()

        return budget is not None

    def close(self):
        self.db.close()
