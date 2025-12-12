from flask import session, redirect, url_for, flash
from functools import wraps

def auth_required(f):
    '''Decorator to ensure that a user is logged in before accessing a route.'''
    
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You need to be logged in to access this page.", "error")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return decorated_function

"""Ensure the user is logged in before accessing the route.
    This decorator checks for 'user_id' in the session.
    If the user is not logged in, they are redirected to the login page."""

def admin_required(f):
    '''To ensure that the logged-in user has admin privileges.'''
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in
        if 'user_id' not in session:
            flash("You need to be logged in to access this page.", "error")
            return redirect(url_for('auth.login'))
        
        # Check if user is admin
        if session.get('role') != 'admin':
            session.clear()
            flash("You do not have permission to access this page.", "error")
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)

    return decorated_function

def doctor_required(f):
    ''' Ensures that the logged-in user has doctor privileges.'''
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # user must be logged in
        if 'user_id' not in session:
            flash("You need to be logged in to access this page.", "error")
            return redirect(url_for('auth.login'))
        # user must be a doctor                                                  
        if session.get('role') != 'doctor':
            session.clear()
            flash("You do not have permission to access this page.", "error")
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)

    return decorated_function

def admin_or_doctor_required(f):
    '''Ensures that the logged-in user has either admin or doctor privileges.'''
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # user must be logged in
        if 'user_id' not in session:
            flash("You need to be logged in to access this page.", "error")
            return redirect(url_for('auth.login'))
        # user must be admin or doctor
        if session.get('role') not in ['admin', 'doctor']:
            session.clear()
            flash("You do not have permission to access this page.", "error")
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)

    return decorated_function