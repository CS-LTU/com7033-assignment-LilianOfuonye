from flask import Blueprint, render_template


# This is the authentication file that handles login, register,logout and home page redirect, with everything grouped within a blueprint.
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/')
def index():
    return render_template('login.html')
