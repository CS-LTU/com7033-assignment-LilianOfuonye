from flask import Blueprint, render_template, request, flash, current_app, session, redirect, url_for
from app.models.user import User
from utils.decorators import auth_required, admin_or_doctor_required, admin_required, doctor_required
from app.models.patient import Patient
import re  
from datetime import datetime
from werkzeug.security import generate_password_hash


dashboard_blueprint = Blueprint('dashboard', __name__)

@dashboard_blueprint.route('/user_dashboard')
@auth_required
@admin_required
def user_dashboard():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    users, total = User.get_paginated_users(page=page, per_page=per_page)
    
    total_pages = (total + per_page - 1) // per_page
    
    return render_template('user_dashboard.html',
                         users=users,
                         page=page,
                         per_page=per_page,
                         total_users=total,
                         total_pages=total_pages,
                         has_prev=page > 1,
                         has_next=page < total_pages)

@dashboard_blueprint.route('/dashboard')
@auth_required
@admin_or_doctor_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    patients, total = Patient.get_paginated_patients(page=page, per_page=per_page)
    
    total_pages = (total + per_page - 1) // per_page
    
    return render_template('dashboard.html',
                         patients=patients,
                         page=page,
                         per_page=per_page,
                         total_patients=total,
                         total_pages=total_pages,
                         has_prev=page > 1,
                         has_next=page < total_pages)

@dashboard_blueprint.route('/register_patient', methods=['GET', 'POST'])
@auth_required
@admin_required
def register_patient():
    if request.method == 'POST':
        try:
            patient_id = int(request.form.get('id', '').strip())
            gender = request.form.get('gender', '').strip()
            age = int(request.form.get('age', '').strip())
            hypertension = int(request.form.get('hypertension', '0'))
            heart_disease = int(request.form.get('heart_disease', '0'))
            ever_married = request.form.get('ever_married', '').strip()
            work_type = request.form.get('work_type', '').strip()
            residence_type = request.form.get('residence_type', '').strip()
            avg_glucose_level = float(request.form.get('avg_glucose_level', '').strip())
            bmi = float(request.form.get('bmi', '').strip())
            smoking_status = request.form.get('smoking_status', '').strip()
            stroke = int(request.form.get('stroke', '0'))
               
            # Basic validation
            if not all([patient_id, gender, age, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status is not None]):
                raise ValueError("All fields are required.")
            
            # Age validation
            if age < 0 or age > 120:
                raise ValueError("Invalid age.")
            
            # Gender validation
            gender_options = ['Male', 'Female']
            if gender not in gender_options:
                raise ValueError("Invalid gender selection.") 
            
            # BMI validation
            if bmi < 10 or bmi > 100:
                raise ValueError("Invalid BMI value.")
            
            # Glucose level validation
            if avg_glucose_level < 0 or avg_glucose_level > 500:
                raise ValueError("Invalid glucose level.")
            
            Patient.create_patient(
                patient_id, gender, age, hypertension, heart_disease,
                ever_married, work_type, residence_type, avg_glucose_level,
                bmi, smoking_status, stroke
            )
            flash("Patient registered successfully!", "success")
            return redirect(url_for('dashboard.dashboard'))
        
        except ValueError as e:
            flash(f"{e}", 'error')
            return redirect(url_for("dashboard.dashboard"))
        except Exception as e:
            flash(f"Error registering patient: {e}", 'error')
            return redirect(url_for("dashboard.dashboard"))
            
            
@dashboard_blueprint.route('/dashboard/patients/<int:patient_id>')
@auth_required
@admin_or_doctor_required
def view_patient(patient_id):
    patient = Patient.get_by_id(patient_id)
    if not patient:
        flash("Patient not found.", "error")
        return redirect(url_for('dashboard.dashboard'))
    return render_template('view_patient.html', patient=patient)


@dashboard_blueprint.route('/dashboard/patients/<int:patient_id>/update', methods=['GET', 'POST'])
@auth_required
@admin_or_doctor_required
def update_patient(patient_id):
    if request.method == 'POST':
        try:
            gender = request.form.get('gender', '').strip()
            age = int(request.form.get('age', '').strip())
            hypertension = int(request.form.get('hypertension', '0'))
            heart_disease = int(request.form.get('heart_disease', '0'))
            ever_married = request.form.get('ever_married', '').strip()
            work_type = request.form.get('work_type', '').strip()
            residence_type = request.form.get('residence_type', '').strip()
            avg_glucose_level = float(request.form.get('avg_glucose_level', '').strip())
            bmi = float(request.form.get('bmi', '').strip())
            smoking_status = request.form.get('smoking_status', '').strip()
            stroke = int(request.form.get('stroke', '0'))
            
            # Basic validation
            if not all([gender, age, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status is not None]):
                raise ValueError("All fields are required.")
            
            # Age validation
            if age < 0 or age > 120:
                raise ValueError("Invalid age.")
            
            # Gender validation
            gender_options = ['Male', 'Female']
            if gender not in gender_options:
                raise ValueError("Invalid gender selection.") 
            
            # BMI validation
            if bmi < 10 or bmi > 100:
                raise ValueError("Invalid BMI value.")
            
            # Glucose level validation
            if avg_glucose_level < 0 or avg_glucose_level > 500:
                raise ValueError("Invalid glucose level.")
            
            Patient.update(
                patient_id, gender, age, hypertension, heart_disease,
                ever_married, work_type, residence_type, avg_glucose_level,
                bmi, smoking_status, stroke
            )
            flash("Patient information updated successfully!", "success")
            return redirect(url_for('dashboard.view_patient', patient_id=patient_id))
        
        except ValueError as e:
            flash(f"{e}", 'error')
            return redirect(url_for('dashboard.view_patient', patient_id=patient_id))
        except Exception as e:
            flash(f"Error updating patient: {e}", 'error')
            return redirect(url_for('dashboard.view_patient', patient_id=patient_id))
        
        
@dashboard_blueprint.route('/dashboard/patients/<int:patient_id>/delete', methods=['POST'])
@auth_required
@admin_required
def delete_patient(patient_id):
    try:
        Patient.delete_patient(patient_id)
        flash("Patient deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting patient: {e}", "error")
    return redirect(url_for('dashboard.dashboard'))

@dashboard_blueprint.route('/register_user', methods=['POST'])
@auth_required
@admin_required
def register_user():
    try:
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', '').strip()
        
        # Basic validation
        if not all([first_name, last_name, email, password, role]):
            raise ValueError("All fields are required.")
        
        # Email validation
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format.")
        
        # Password validation
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        
        # Role validation
        role_options = ['admin', 'doctor']
        if role not in role_options:
            raise ValueError("Invalid role selection.")
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        User.create_user(first_name, last_name, email, password_hash, role)
        flash("User registered successfully!", "success")
        return redirect(url_for('dashboard.user_dashboard'))
    
    except ValueError as e:
        flash(f"{e}", 'error')
        return redirect(url_for("dashboard.user_dashboard"))
    except Exception as e:
        flash(f"Error registering user: {e}", 'error')
        return redirect(url_for("dashboard.user_dashboard"))

@dashboard_blueprint.route('/dashboard/users/<user_id>')
@auth_required
@admin_required
def view_user(user_id):
    user = User.get_by_id(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('dashboard.user_dashboard'))
    return render_template('view_user.html', user=user)

@dashboard_blueprint.route('/dashboard/users/<user_id>/update', methods=['POST'])
@auth_required
@admin_required
def update_user(user_id):
    try:
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        role = request.form.get('role', '').strip()
        
        # Basic validation
        if not all([first_name, last_name, role]):
            raise ValueError("All fields are required.")
        
        # Role validation
        role_options = ['admin', 'doctor']
        if role not in role_options:
            raise ValueError("Invalid role selection.")
        
        User.update(user_id, first_name, last_name, role)
        flash("User information updated successfully!", "success")
        return redirect(url_for('dashboard.user_dashboard'))
    
    except ValueError as e:
        flash(f"{e}", 'error')
        return redirect(url_for('dashboard.user_dashboard'))
    except Exception as e:
        flash(f"Error updating user: {e}", 'error')
        return redirect(url_for('dashboard.user_dashboard'))

@dashboard_blueprint.route('/dashboard/users/<user_id>/delete', methods=['POST'])
@auth_required
@admin_required
def delete_user(user_id):
    try:
        # Prevent deleting yourself
        if session.get('user_id') == user_id:
            flash("You cannot delete your own account.", "error")
            return redirect(url_for('dashboard.user_dashboard'))
        
        User.delete_user(user_id)
        flash("User deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting user: {e}", "error")
    return redirect(url_for('dashboard.user_dashboard'))

