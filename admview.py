from flask import (
    Blueprint, Flask, g, redirect, render_template
)

from datetime import datetime

from switchfx.db import get_db
from switchfx.admin import AppAdmin

bp = Blueprint('admview', __name__, url_prefix='/admview')
db = get_db()

@bp.route('index', methods=('GET', 'POST'))
def dash():

        users = AppAdmin(get_db).get_users(db)
        comments = AppAdmin.get_coms(db)

        return render_template('dashboard.html', users= users, comments=comments)



def del_coms_thrd_user():
    if request.method == 'POST':
        user_name = request.form['thread_id']
        password = request.form['user_name']
        

        user = db.execute(
            'SELECT * FROM user WHERE user_name = ?', (user_name,)
        ).fetchone()

       

        flash(error)
    return render_template('auth/login.html', form = form)
