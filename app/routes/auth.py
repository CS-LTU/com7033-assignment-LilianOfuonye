import sqlite3
from flask import Blueprint, flash, request, redirect, render_template, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import re
from app.config.sqlite import get_user_by_email

"""
This is the authentication file that handles login, register,logout 
and home page redirect, with everything 
grouped within a blueprint.

"""

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/')
def index():
    return render_template('landing_page.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')

            if not email or not password:
                raise ValueError ("All fields are required.")
                

            user = get_user_by_email(email)
            if not user :
                raise ValueError('user doesnt exist')
    
            if not check_password_hash(user.password_hash, password):
                raise ValueError("Invalid email or password.")
            
            session['user_id'] = user.id
            session['role'] = user.role
            session.permanent = True
            flash("Login successful!", "success")
            return redirect(url_for('dashboard.dashboard'))

        
        except ValueError as e:
            flash(f"{e}", 'error')
            return redirect(url_for("auth.login"))
        
    return render_template('login.html')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
     if request.method == 'POST':
        try:
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            role = request.form.get('role')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            # Basic validation
            if not all([first_name, last_name, email, password, confirm_password]):
                raise ValueError ("All fields are required.")
               
            if password != confirm_password:
                raise ValueError ("Passwords do not match.")
            
            # Email pattern validation
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_pattern, email):
                raise ValueError('Please enter a valid email address') 
            
            # Password strength validation
            pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$'
            if not re.match(pattern, password):
                raise ValueError('Password must be 8+ chars and include upper, lower, digit and special char.')
                
            if get_user_by_email(email):
                raise ValueError ("A user with this email already exists. Choose another.")
            
            # Hash the password
            hashed_password = generate_password_hash(password)

            # Save to SQLite
            with sqlite3.connect("london_health.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (first_name, last_name, email, role, password_hash) VALUES (?, ?, ?, ?, ?)", (first_name, last_name, email, role, hashed_password))
                conn.commit()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('auth.login'))
        except ValueError as error:
            flash(f"{error}", 'error')
            return render_template('register.html')


     return render_template('register.html')
     


@auth_blueprint.route('/logout')
def logout():
    session.pop("email", None)
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
