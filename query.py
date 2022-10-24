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
        'SELECT u.first_name, ft.base_currency, ft.quote_currency, ft.exchange_rate_cury, ft.base_exchange, ft.amount, ft.exchange_rate, ft.payment_method, \
        ft.comment, ft.user_name, ft.created_on'
        ' FROM forex_thread ft JOIN user u ON ft.user_id=u.id'
        ' ORDER BY ft.created_on DESC LIMIT ? OFFSET ? ', (lm,of,) 
        ).fetchall()

        return forex_thread

    def row_count(self):
        row_count = self.db.execute('SELECT COUNT(*) FROM forex_thread')
        results = row_count.fetchone()
        total =  results[0]
        total = total + 40 # added to simulate large row count
        return total
    
    def paginate(self, off_set=5, row_count=100, lm=10 ):
         link_array = list(range(off_set, row_count, lm))
         last_element = link_array[-1]
         #check to see if additonal element(offset) should be appended to the list
         if ( row_count > last_element):
            extra_elem = row_count - last_element
            extra_elem = extra_elem + last_element
            link_array.append(extra_elem)
            return link_array
         else:
            link_array = list(range(off_set, row_count, lm))
            return link_array
    
    def next_off_set(self, link_array,  url_off_set):
        if(link_array[3] == url_off_set):
            off_set = url_off_set
            return off_set
        else:
            return False

        


            
   
        
