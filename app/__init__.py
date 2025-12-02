from flask import Flask
from dotenv import load_dotenv
from app.config.sqlite import init_db
import os

load_dotenv()

# Add app factory with DB initialisation and blueprint registration
"""This is where the flask app is created. It would function as a central point that holds 
everything together """


def create_app():
    # Load values from .env into environment variable
    
    app = Flask(__name__)

    # Database setup
    init_db()

    # Read secret key 
    app.secret_key = os.getenv("SECRET_KEY")
    print(app.secret_key)
    from app.routes import auth
    from app.routes import dashboard

    # Blueprint registration to make the route active in the app
    app.register_blueprint(auth.auth_blueprint)
    app.register_blueprint(dashboard.dashboard_blueprint)


    return app