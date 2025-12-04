from flask import Blueprint, render_template, request, flash, current_app, session, redirect, url_for
from utils.decorators import auth_required, admin_or_doctor_required, admin_required, doctor_required
from app.models.patient import Patient
import re  
from datetime import datetime


dashboard_blueprint = Blueprint('dashboard', __name__)

@dashboard_blueprint.route('/dashboard')
@auth_required
@admin_or_doctor_required
def dashboard():
    patients = Patient.get_all_patients()  
    return render_template('dashboard.html', patients=patients)

@dashboard_blueprint.route('/register_patient', methods=['GET', 'POST'])
@auth_required
@admin_required
def register_patient():
    if request.method == 'POST':
        try:
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            date_of_birth = request.form.get('date_of_birth', '').strip()
            gender = request.form.get('gender', '').strip()
            email = request.form.get('email', '').strip().lower()
               
            # Basic validation
            if not all([first_name, last_name, date_of_birth, gender, email]):
                raise ValueError ("All fields are required.")
            
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_pattern, email):
                raise ValueError("Invalid email format.")
            
            # Validate date of birth
            dob = datetime.strptime(date_of_birth, '%Y-%m-%d')
            today = datetime.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 0 or age > 120:
                raise ValueError("Invalid date of birth.")
            
            # gender validation
            gender_options = ['Male', 'Female', 'Other']
            if gender not in gender_options:
                raise ValueError("Invalid gender selection.") 
            
            Patient.create_patient(first_name, last_name, date_of_birth, gender, email)
            flash("Patient registered successfully!", "success")
            return redirect(url_for('dashboard.dashboard'))
        
        except ValueError as e:
            flash(f"{e}", 'error')
            return redirect(url_for("dashboard.dashboard"))
            
            
@dashboard_blueprint.route('/dashboard/patients/<int:patient_id>')
@auth_required
@doctor_required
def view_patient(patient_id):
    patient = Patient.get_by_id(patient_id)
    if not patient:
        flash("Patient not found.", "error")
        return redirect(url_for('dashboard.dashboard'))
    return render_template('view_patient.html', patient=patient)


@dashboard_blueprint.route('/dashboard/patients/<int:patient_id>/update', methods=['GET', 'POST'])
@auth_required
@doctor_required
def update_patient(patient_id):
    if request.method == 'POST':
        try:
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            date_of_birth = request.form.get('date_of_birth', '').strip()
            gender = request.form.get('gender', '').strip()
            
            # Basic validation
            if not all([first_name, last_name, date_of_birth, gender]):
                raise ValueError("All fields are required.")
            
            # Validate date of birth
            dob = datetime.strptime(date_of_birth, '%Y-%m-%d')
            today = datetime.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 0 or age > 120:
                raise ValueError("Invalid date of birth.")
            
            # gender validation
            gender_options = ['Male', 'Female', 'Other']
            if gender not in gender_options:
                raise ValueError("Invalid gender selection.") 
            
            Patient.update(patient_id, first_name, last_name, date_of_birth, gender)
            flash("Patient information updated successfully!", "success")
            return redirect(url_for('dashboard.view_patient', patient_id=patient_id))
        
        except ValueError as e:
            flash(f"{e}", 'error')
            return redirect(url_for('dashboard.view_patient', patient_id=patient_id))
