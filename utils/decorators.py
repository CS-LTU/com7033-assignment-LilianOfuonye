from flask import session, redirect, url_for, flash
from functools import wraps

def auth_required(f):
    '''Decorator to ensure that a user is logged in before accessing a route.'''
    
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("You need to be logged in to access this page.", "error")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return decorated_function
