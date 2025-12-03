from flask import Blueprint, render_template, current_app, session, redirect, url_for
from utils.decorators import auth_required



dashboard_blueprint = Blueprint('dashboard', __name__)

@dashboard_blueprint.route('/dashboard')
@auth_required
def dashboard():
    
   
    return render_template('dashboard.html')
