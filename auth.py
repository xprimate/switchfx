import os
from dotenv import load_dotenv
import functools
import re 
from datetime import datetime
from switchfx.forms import LoginForm
from switchfx.forms import RegisterForm

from switchfx.forms import ResetEmailForm
from switchfx.forms import ResetPasswordForm
from switchfx.mail import send_mails, reset_mail
from itsdangerous import URLSafeTimedSerializer

from werkzeug.exceptions import abort



from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from switchfx.db import get_db

load_dotenv()

bp = Blueprint('auth', __name__, url_prefix='/auth')

ts = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))


#Client ip address
def client_ip():
    ip = request.environ.get('HTTP_xFORWARDED_FOR', request.remote_addr)
    return ip

#Email address validation
def email_valide(email):
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))


#User Registration
@bp.route('register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if request.method == 'POST':
        user_name = request.form['user_name']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        email    = request.form['email']
        db = get_db()
        error = None

        if not user_name:
            error = 'Username is required.'
        if len(user_name) < 4:
            error = 'Username is too short'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required'
        elif not first_name:
            error = 'Firstname is required'
        elif not last_name:
            error = 'Lastname is required'
            
        if error is None:
            user_status = 'ACTIVE'
            created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            last_activity = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            status = 'NONE'
            updated_on = 'NONE'
            ip = client_ip()
        

            try:
                db.execute(
                "INSERT INTO user (user_name, first_name, last_name, email,\
                 password, user_status, status, created_on, last_activity, ip, updated_on) VALUES (?,?,?,?,?,?,?,?,?,?,?)",\
                 (user_name, first_name, last_name, email, generate_password_hash(password), user_status, status, created_on, last_activity, ip, updated_on),)
                db.commit()
            except db.IntegrityError:
                
               error = f"User {user_name} or email is already registered."
                
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template('auth/register.html', form = form)

@bp.route('login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        

        db = get_db()
        error = None
        
        # Fetch user record with username or email if email is typed in
        user = db.execute(
            'SELECT * FROM user WHERE user_name = ?', (user_name,)
        ).fetchone()
       
        if user is None:
            error = 'Incorrect Username/pasword.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect username/password.'
        

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['user_name'] = user['user_name'] 
            session['email'] = user['email'] 
            session['user_firstname'] = user['first_name']
            session['user_lastname'] = user['last_name'] 
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html', form = form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

# Pasword Reset Email 
@bp.route('reset', methods=["GET", "POST"])
def reset():
    form = ResetEmailForm()
    db = get_db()

   # if request.method == 'POST':
    if form.validate_on_submit():
        email = form.email.data
        #user = User.query.filter_by(email=form.email.data).first_or_404()
        users = db.execute(
            'SELECT email, first_name FROM user WHERE email = ?', (email,)
        ).fetchone()
        
        if users is None:
            flash("Your email is not yet registered", "alert-warning")
            return redirect(request.referrer)
        else:
            token = ts.dumps(email, salt='recover-key')
            recovery_url = url_for('auth.resetpwd',token=token, _external=True)
            flash("Mail sent, Please Check your Email(and spam box) for detail.", "alert-success")
            reset_mail(users, recovery_url)
      
        

        return redirect(url_for('index'))
    return render_template('auth/reset.html', form=form)


@bp.route('/resetpwd/<token>', methods=["GET", "POST"])
def resetpwd(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = ResetPasswordForm()
    db = get_db()
    
    if form.validate_on_submit():
        user = db.execute(
            'SELECT email, first_name FROM user WHERE email = ?', (email,)
        ).fetchone()
        hash_paswd = generate_password_hash(form.password.data)
        
        db.execute(
                'UPDATE user SET password = ?'
                ' WHERE email = ?',
                (hash_paswd, user['email'])
            )
        db.commit()
        flash('Your Password has been updated Succefully', 'alert-success')
    
        return redirect(url_for("auth.login"))

    return render_template('auth/pw_rst.html', form=form, token=token)