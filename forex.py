from flask import (
    Blueprint, Flask, g, redirect, render_template, request, url_for, session, flash,
)
from decimal import *
from datetime import datetime
from werkzeug.exceptions import abort

from switchfx.admin import AppAdmin

from switchfx.auth import login_required
from switchfx.auth import client_ip
from switchfx.db import get_db
from switchfx.query import PostComment, ForexThread
from switchfx.mail import send_mails, mail_thread_owner
import time

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

# Get the thread id from the request url
def get_thread_id(request_referrer):
    referrer_url = request_referrer
    thread_id = referrer_url.split("thread_id=",1)[1]
    #thread_id = referrer_url[-1]
    thread_id =  int(thread_id)
    return thread_id

@bp.route('/')
def index():
    
    #Grabs the request arges
    url_limit = request.args.get('limit')
    url_off_set = request.args.get('off_set')
    url_next = request.args.get('next')
    url_prev = request.args.get('prev')
    #Returns the forex_thread row count
    row_count= forex_thread = ForexThread(get_db()).row_count()
    # Calculate the next offset to used when the "Next" Button is clicked
    #Ensures that the request arges is a number and it is not None.

    #REDO THIS WHO OFFSET AND PAGINATION ALGORITHM
    if not (isInt(url_limit, url_off_set) ):
         #Default limit and offset
        url_limit = 100
        url_off_set = 100
    #check for Next button click and recalculate the offset
    if(url_next != None):
        off_set = url_next
        url_off_set = off_set
    else:
        off_set = 100
    if(url_prev != None):
        off_set = int(url_prev)
        print(url_prev)
        url_off_set = off_set
    else:
        off_set =100
    #Generate the limit to go into each pagination button in a list
    link_array = ForexThread(get_db()).paginate(off_set, row_count=5000, lm=100)


    # @param 1 -limit @param 2 offset
    forex_thread = ForexThread(get_db()).get_forex_thread(url_limit=100,url_off_set=0)
    return render_template('forex/index.html', forex_thread=forex_thread, link_array=link_array)


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
        base_exchange  = request.form.get('base_exchange')
        payment_method        = request.form.getlist('payment')
 
        error          = None

        user_id = session.get('user_id')
        user_name = session.get('user_name')
        user_email = session.get('email')
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
        elif not exchange_rate_cury:
            error = 'Exchange rate currency is required, please reset'
        elif not payment_method:
            error = 'Please select at least on payment option'
        elif not base_exchange:
            error = '/ currency is required'
        
        if error is not None:
            flash(error)
        
        else:
            amount_to_be_sent =  exchange_amount(exchange_rate_cury, quote_currency, base_currency, exchange_rate, amount)
            payment_method = "|".join(payment_method)
            ip = client_ip()
            status = 'ACTIVE'
            created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

          
            db = get_db()
            db.execute(
                "INSERT INTO forex_thread (user_id, base_currency, quote_currency, amount, exchange_rate,\
                 exchange_rate_cury, base_exchange, payment_method, comment, ip, email, user_name, status, created_on)\
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user_id, base_currency, quote_currency, amount_to_be_sent, exchange_rate, exchange_rate_cury, base_exchange, payment_method, comment,
                ip, user_email, user_name, status, created_on)
            )
            db.commit()
            

            flash("Your Post is successful!", "alert-success")
            return redirect(url_for('forex.index'))

    return render_template('forex/create.html')


@bp.route('/post_comment', methods=('GET', 'POST'))
def post_comment():
    if request.method == 'POST':
        
        comment        = request.form.get('comment')
       
        if  session.get('user_id'):
            user_id = session.get('user_id')
            user_name = session.get('user_name')
            email = session.get('email')
           
        else:
            user_id = 'NONE'
            guest ='guest_'
            user_name = request.form.get('user_name')
            user_name = '{}_{}'.format(guest, user_name)  #append guest to the user_name 
            email = request.form.get('email')
            user_name_and_email = '' #make show/require user_name and email form in template

        error          = None

        ip      = client_ip()
        status  = 'ACTIVE'
        created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        thread_id = get_thread_id(request.referrer)


        if not user_name:
            error = 'Please Enter your Username.'
          
        elif not email:
            error = 'Please enter your email.'
        elif not comment:
            error = 'Please write a comment.'
        elif not get_thread_id(request.referrer):
            error = "Issue with your request, please try again later"
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            avatar = PostComment.avatar(email, 64)
            post_comment = PostComment.post_comment(db, comment, user_id, thread_id, created_on,
            user_name, email, status, ip, avatar )

            #Notifying users about the comment
            comment_users = PostComment.get_forex_thread_comment_users(db, thread_id)
            thread_owner_user_name = session.get('thread_owner_user_name')
            thread_owner_email = session.get('thread_owner_email')
            
            
            message = "Follow the link to view: " + request.referrer

            #email commenters 
            
            #convert to set to avoid duplicates
            send_mails(set(comment_users), message)
            flash("Your comment is successful!", "alert-success")

            #mail thread owner or stop if the email is contained in comment_users list
            for comment_user in comment_users:
                #mail_thread_owner(thread_owner_user_name, thread_owner_email, message) if thread_owner_email  in  comment_user['email'] else {} 
                if thread_owner_email  in  comment_user['email']:
                    pass  
                else:
                    {
                    mail_thread_owner(thread_owner_user_name, thread_owner_email, message)
                    }

            


        return redirect(request.referrer)


        if not post_comment:
            flash('Sorry, something went wrong, try again later.')
        elif not avatar:
            flash('Sorry can not load avatar')

        return redirect(request.referrer)

            
    
    return redirect(request.referrer)


@bp.route('/get_comment', methods=('GET', 'POST'))
def get_comment():
    
    if  request.method == 'GET':
            url_thread_id = request.args.get('thread_id')
            url_thread_id = int(url_thread_id)

            #Hide/require input if user is logged in or not
            user_name_and_email = ''
            input_required = 'required'
            user_id = session.get('user_id')
            if  user_id:
                user_name_and_email = 'hidden'
                input_required = ''
            
            db = get_db()
            
            # Fetch a single forex_thread_post
            forex_thread_single = PostComment.get_forex_thread_single(db, url_thread_id)
            forex_thread_comment = PostComment.get_forex_thread_comment(db, url_thread_id)

            #get the email and user name of the thread poster 
            thread_owner_email = forex_thread_single['email']
            thread_owner_user_name = forex_thread_single['user_name']
            session['thread_owner_email'] = thread_owner_email
            session['thread_owner_user_name'] = thread_owner_user_name

            ## Add an if statement to catch error in "forex_thread_single" and "forex_thread_comment"
            return render_template('forex/get_comment.html',  forex_thread_single = forex_thread_single,
             forex_thread_comment = forex_thread_comment, user_name_and_email = user_name_and_email,
              input_required = input_required,  len = len(forex_thread_comment))


    return redirect(request.referrer)

@login_required
@bp.route('/user_forex', methods=('GET', 'POST'))
@login_required
def user_forex():
    
    if  request.method == 'GET':
        user_forex_thread = ForexThread(get_db()).get_user_forex_thread(session['user_id'])

        return render_template('forex/user_forex.html', user_forex_thread= user_forex_thread)


# Admin Interface        
@bp.route('/wkno9g68zqhy13yd5kxl', methods=('GET', 'POST')) 
@login_required   
def wkno9g68zqhy13yd5kxl():
        url_limit = 100
        url_off_set = 0

        if request.args.get('limit') and request.args.get('offset'):
            url_limit = request.args.get('limit')
            url_off_set = request.args.get('offset')

        users = AppAdmin.get_users(get_db(), url_limit, url_off_set)
        comments = AppAdmin.get_coms(get_db(), url_limit, url_off_set)


        if  request.method == 'POST':
            if request.form['bt_delete'] == 'Delete2':
                url_thread_id=request.form['thread_id']
                url_thread_id =  int(url_thread_id)
                url_user_name = request.form['user_name']
                result = AppAdmin.del_coms_thrd_user(get_db(), url_thread_id, url_user_name)
                if result:
                    flash('Success!')
                    return redirect(request.referrer)
                else:
                    flash('Failed to Delete!')
                    return redirect(request.referrer)

            
            elif request.form['bt_delete'] == 'Delete1':
                url_user_name = request.form['user_name']
                result = AppAdmin.del_coms_user(get_db(), url_user_name)
                if result:
                    flash(result)
                    return redirect(request.referrer)
                else:
                    flash('Failed to Delete!')
                    return redirect(request.referrer)

            elif request.form['bt_delete'] == 'DeleteID':
                comment_id = int(request.form['comment_id'])
                result = AppAdmin.del_coms_id(get_db(), comment_id)
                if result:
                    flash('Success!')
                    return redirect(request.referrer)
                    flash('Sorry, Unable to Delete')
                else:
                    flash('Failed to Delete!')
                    return redirect(request_referrer)
            
            elif request.form['bt_delete'] == 'DeleteThread':
                thread_id = int(request.form['forex_thread_id'])
                result = AppAdmin.del_forex_thread(get_db(), thread_id)
                if result:
                    flash('Success!')
                    return redirect(request.referrer)
                else:
                    flash('Failed to Delete!')
                    return redirect(request_referrer)
            
            elif request.form['bt_delete'] == 'ArchiveThread':
                thread_id = int(request.form['forex_thread_archive'])
                result = AppAdmin.archive_thread(get_db(), thread_id)
                if result:
                    flash('Success!')
                    return redirect(request.referrer)
                else:
                    flash('Failed to Delete!')
                    return redirect(request_referrer)
            
            elif request.form['bt_delete'] == 'DeleteUser':
                user_id = int(request.form['user_id'])
                result = AppAdmin.delete_user(get_db(), user_id)
                if result:
                    flash('Success!')
                    return redirect(request.referrer)
                else:
                    flash('Failed to Delete!')
                    return redirect(request_referrer)


        return render_template('dashboard.html', users= users, comments=comments)

#Delet comment by user_name and user ID
@bp.route('/del_coms_2', methods=('GET','POST'))
def del_coms_2():
    return print("Mr valide Response")



   
            #url_thread_id = request.args.get('thread_id')
            #url_thread_id = int(url_thread_id)
            #url_user_name = request.args.get('user_name')

    #print(url_thread_id)

            


     
    

                
