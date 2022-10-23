from flask import render_template
from switchfx.forms import LoginForm
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from switchfx.db import get_db

bp = Blueprint('signin', __name__, url_prefix='/signin')


@bp.route('/sign')
def login():
    form = BSFormField()
    return render_template('auth/signin.html', title='Sign In', form=form)

