from flask import (
    Blueprint, Flask, g, redirect, render_template, request, url_for
)
from datetime import datetime
from werkzeug.exceptions import abort

from switchfx.auth import login_required
from switchfx.auth import client_ip
from switchfx.db import get_db

bp = Blueprint('forex', __name__)

@bp.route('/')
def index():
    db = get_db()
    forex_thread = db.executed(
        'SELECT u.first_name base_currency, quote_currency, amount, exchange_rate,payment_method,\
        comment,user_name,created_on'
        'FROM forex_thread ft JOIN user u ON ft.user_id=u.id'
        'ORDER BY created_on, DESC'
    ).fetchall()
    return render_template('forex/index.html', forex_thread=forex_thread)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        base_currency  = request.form['base_currency']
        quote_currency = request.form['quote_currency']
        amount         = request.form['amount']
        exchange_rate  = request.form['exchange_rate']
        payment_method = request.form['payment_method']
        comment        = request.form['comment']
        user_name      = request.form['username']
        created_on     = request.form['created_on']
        error          = None

        user_id = g.user_id
        user_name = g.user_name
        ip      = client_ip()
        status  = 'ACTIVE'
        created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not base_currency:
            error = 'Base Currency is required.'
        elif not quote_currency:
            error = 'Quote Currency is required.'
        elif not amount:
            error = 'Amount is required.'
        elif not exchange_rate:
            error = 'Exchange rate is reuired.'
        
        if error is not None:
            flash(error)
        
        else:
            db = get_db()
            db.execute(
                'INSERT INTO forex_thread (user_id, base_currency, quote_currency,amount,exchange_rate,\
                payment_method,comment,ip,user_name,status,created_on)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (user_id, base_currency, quote_currency, amount, exchange_rate, payment_method, comment,
                ip, user_name, status, created_on)
            )
            db.commit()
            return redirect(url_for('forex.index'))

    return render_template('forex/create.html')