from flask import request
from switchfx.db import get_db 

class ForexThread():
    #def __init__(self, db = db limit=10, offset=10, order = 'DESC'):

    def __init__(self, db):
        #self.limit = limit
        #self.range = range
        self.db = db
       # db = get_db()

    def get_forex_thread(self, lm=5, of=0):
        lm = lm
        of =of
        forex_thread = self.db.execute(
        'SELECT u.first_name, ft.base_currency, ft.quote_currency, ft.amount, ft.exchange_rate, ft.payment_method, \
        ft.comment, ft.user_name, ft.created_on'
        ' FROM forex_thread ft JOIN user u ON ft.user_id=u.id'
        ' ORDER BY ft.created_on DESC LIMIT ? OFFSET ? ', (lm,of,) 
        ).fetchall()

        return forex_thread

    def row_count(self):
        row_count = self.db.execute('SELECT COUNT(*) FROM forex_thread')
        return row_count


            
   
        
