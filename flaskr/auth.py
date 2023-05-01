import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for);
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.models.user import User
from flaskr.db import db_session

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register(): 
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        error = None

        if email is None:
            error = 'email is required'
        elif password is None:
            error = 'password is required'
        user = User.query.filter_by(email=email).first()
        if user is not None:
            error = 'Email has been registered!!!'
        if error is None:
            user = User(name=name, email=email, password=generate_password_hash(password))
            db_session.add(user)
            db_session.commit()
            flash('User has been registered')
        else:
            flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        user = User.query.filter_by(email=email).first()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user_id'] = user.id
            g.user = user
            return redirect(url_for('blog.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))