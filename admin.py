from flask import request
from hashlib import md5
from switchfx.db import get_db 



class AppAdmin():

    
    def get_users(db, limit, offset):
        users = db.execute("SELECT * FROM user").fetchall() # Add the offset and limit when you have more users
        return users

    
    def del_users(db, user_name):
        db.execute("DELETE FROM user WHERE  user_name = ?", (user_name,))
    
    def del_coms_user(db, user_name):  
        db.execute('DELETE FROM forex_thread_post WHERE  user_name = ?', (user_name,))
        db.commit()
        return True
        # find a way to confirm that the commite is succesfull

    
    def del_coms_thrd_user(db, thread_id, user_name):
        db.execute('DELETE FROM forex_thread_post WHERE thread_id = ? AND user_name = ? ', (thread_id, user_name,))
        db.commit()
        return True
        # find a way to confirm that the commite is succesfull
    
    def del_coms_id(db, id):
        db.execute('DELETE FROM forex_thread_post WHERE  id = ?', (id,))
        db.commit()
        return True
        # find a way to confirm that the commite is succesfull
        
    
    def get_coms(db, limit, offset):
        comments = db.execute("SELECT * FROM forex_thread_post ORDER BY created_on  DESC LIMIT ? OFFSET ?",(limit, offset,)).fetchall()
        return comments



            

