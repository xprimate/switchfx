from flask import (
    Blueprint, Flask, g, redirect, render_template, request, url_for, session, flash,
)
from decimal import *
from datetime import datetime
from datetime import datetime
from werkzeug.exceptions import abort

from switchfx.auth import login_required
from switchfx.auth import client_ip
from switchfx.db import get_db
from switchfx.query import ForexThread

bp = Blueprint('forex', __name__)

## calculate the amount that will be posted
def exchange_amount(exchange_rate_cury, quote_currency, base_currency, exchange_rate, amount):
    getcontext().prec = 2
    if exchange_rate_cury == quote_currency:
        amount_to_be_sent = float(amount) * float(exchange_rate)
        return round(amount_to_be_sent, 2)

    elif (exchange_rate_cury == base_currency):
        amount_to_be_sent = float(amount) / float(exchange_rate)
        return round(amount_to_be_sent, 2)

## test to see if the string is convertible to float
def string_float(amount, exchange_rate):
    try:
        error_value = 0
        float(amount)
        float(exchange_rate)
    except ValueError:
        error_value = 1
    if(error_value == 1):
        return False
    else:
        return True
    
#Check to see if the variable is integer
    
def isInt(lm, of):
    if((lm is None) or (of is None)):
        return False
    try:
        error_value = 0
        int(lm)
        int(of)
    except ValueError:
        error_value = 1
    if(error_value == 1):
        return False
    else:
         return True
    return False

    

@bp.route('/')
def index():
    
    ## Testing
    #return '''<h1>The query limit is: {}</h1>'''.format(limit)

    #To be gotten from the database
    row_count= forex_thread = ForexThread(get_db()).row_count()

    url_limit = request.args.get('limit')
    url_off_set = request.args.get('off_set')
    
    if not (isInt(url_limit, url_off_set) ):
         #Default limit and offset
        url_limit = 5
        url_off_set = 0


    # @param 1 -limit @param 2 offset
    forex_thread = ForexThread(get_db()).get_forex_thread(url_limit,url_off_set)
    return render_template('forex/index.html', forex_thread=forex_thread, row_count=row_count)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        base_currency  = request.form.get('base_currency')
        quote_currency = request.form.get('quote_currency')
        amount         = request.form.get('send_amount')
        exchange_rate  = request.form.get('exchange_rate')
        exchange_rate_cury = request.form.get('exchange_rate_cury')
        comment        = request.form.get('comment')
        user_name      = request.form.get('username')
        
        payment_method        = request.form.getlist('payment')
 
        error          = None

        user_id = session.get('user_id')
        user_name = session.get('user_name')
        ip      = client_ip()
        status  = 'ACTIVE'
        created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not base_currency:
            error = 'Base Currency is required.'
        elif not quote_currency:
            error = 'Quote Currency is required.'
        elif not amount:
            error = 'Amount is required.'
        elif not string_float(amount, exchange_rate):
            error = 'Please amount must be a real number'    
        elif not exchange_rate:
            error = 'Exchange rate is required.'
        elif not payment_method:
            error = 'Please select at least on payment option'

        
        #
        
        if error is not None:
            flash(error)
        
        else:
            amount_to_be_sent =  exchange_amount(exchange_rate_cury, quote_currency, base_currency, exchange_rate, amount)
            payment_method = "-".join(payment_method)
            ip = client_ip()
            status = 'ACTIVE'
            created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            
            db = get_db()
            db.execute(
                "INSERT INTO forex_thread (user_id, base_currency, quote_currency, amount, exchange_rate,\
                exchange_rate_cury, payment_method, comment, ip, user_name, status, created_on)\
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user_id, base_currency, quote_currency, amount_to_be_sent, exchange_rate, exchange_rate_cury, payment_method, comment,
                ip, user_name, status, created_on)
            )
            db.commit()
            flash("Your Post is successful!")
            return redirect(url_for('forex.index'))

    return render_template('forex/create.html')