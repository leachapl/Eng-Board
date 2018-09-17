import functools, base64

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)

from . import jira

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        auth_str = '' + username + ':' + password + ''
        auth = base64.b64encode(auth_str.encode()).decode('UTF-8')
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required'
        elif not jira.check_login(auth):
            error = 'Invalid username/password combination'
        
        if error is None:
            session.clear()
            session['username'] = username
            session['auth'] = auth
            return redirect(url_for('dashboard.index'))
        
        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')
    auth = session.get('auth')
    if username is None:
        g.user = None
    else:
        g.user = {'username': username, 'auth': auth}

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)

    return wrapped_view

def rest_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return abort(401)
        
        return view(**kwargs)

    return wrapped_view
