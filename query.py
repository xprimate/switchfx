from flask import request
from hashlib import md5
from switchfx.db import get_db 



class ForexThread():
    #def __init__(self, db = db limit=10, offset=10, order = 'DESC'):

    def __init__(self, db):
        #self.limit = limit
        #self.range = range
        self.db = db
       # db = get_db()

    def get_forex_thread(self, url_limit, url_off_set):
       
        forex_thread = self.db.execute(
        'SELECT u.first_name, ft.base_currency, ft.quote_currency, ft.exchange_rate_cury, ft.base_exchange, ft.amount, ft.exchange_rate, ft.payment_method, \
        ft.comment, ft.user_name, ft.created_on, ft.id'
        ' FROM forex_thread ft JOIN user u ON ft.user_id=u.id  '
    
        'WHERE ft.status = ? ORDER BY ft.created_on DESC LIMIT ? OFFSET ? ', ('ACTIVE', url_limit,url_off_set,) 
        ).fetchall()

        return forex_thread

    def get_user_forex_thread(self, user_id):
        user_threads = self.db.execute(
        'SELECT base_currency, quote_currency, exchange_rate_cury, base_exchange, amount, exchange_rate, payment_method, comment, \
        created_on, id FROM forex_thread  WHERE  user_id = ? ORDER BY created_on DESC LIMIT ?', (user_id,100,)).fetchall()
        return user_threads

    

    def row_count(self):
        row_count = self.db.execute('SELECT COUNT(*) FROM forex_thread')
        results = row_count.fetchone()
        total =  results[0]
        total = total + 40 # added to simulate large row count
        return total
    
    def paginate(self, off_set=100, row_count=5000, lm=100 ):
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


class PostComment():
    
    def post_comment(db, commment, user_id, thread_id, created_on,
            user_name, email, status, ip, avatar):
        db.execute(
        "INSERT INTO forex_thread_post (comment, thread_id, user_id, created_on, user_name,\
            email, status, ip, avatar)\
            VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)",
        (commment, thread_id, user_id, created_on, user_name, email, status, ip, avatar )
        )
        db.commit()
        return True

    def get_forex_thread_comment(db, thread_id):
        forex_thread_comment = db.execute('SELECT comment, created_on, user_name, status, avatar FROM \
         forex_thread_post WHERE thread_id = ? ORDER BY created_on  DESC LIMIT ? ', (thread_id, 100,)  ).fetchall()
        return forex_thread_comment
    
    def get_forex_thread_comment_users(db, thread_id):
        forex_thread_comment_users = db.execute('SELECT DISTINCT user_name, email FROM forex_thread_post WHERE thread_id = ? ', (thread_id,)  ).fetchall()
        return forex_thread_comment_users


    def avatar(email='user@paidin.net', size=64):
            digest = md5(email.lower().encode('utf-8')).hexdigest()
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
                digest, size)


    def get_forex_thread_single(db, thread_id):
       
        forex_thread_single = db.execute(
        'SELECT * from forex_thread WHERE id = ?', (thread_id,) 
        ).fetchone()
        return forex_thread_single