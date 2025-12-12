from flask import Flask
from dotenv import load_dotenv
from app.config.sqlite import init_db
from app.config.mongo_db import mongo_init_db
import os
from flask_wtf.csrf import CSRFProtect
from app.config.mongo_seed import seed_mongo

load_dotenv()

# Add app factory with DB initialisation and blueprint registration
"""This is where the flask app is created. It would function as a central point that holds 
everything together """


def create_app():
    # Load values from .env into environment variable
    
    app = Flask(__name__)

    # Database setup
    init_db()
    mongo_init_db()
    seed_mongo()
    
    # Read secret key 
    app.secret_key = os.getenv("SECRET_KEY")
    
    csrf = CSRFProtect(app)
    
    # IMPORTANT: Configure CSRF to protect all POST requests
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_CHECK_DEFAULT'] = True
    
    print(app.secret_key)
    from app.routes import auth
    from app.routes import dashboard

    # Blueprint registration to make the route active in the app
    app.register_blueprint(auth.auth_blueprint)
    app.register_blueprint(dashboard.dashboard_blueprint)

    # Provide current_user in all templates
    @app.context_processor
    def inject_user():
        """Make the logged-in user available to all templates as 'current_user'."""
        from flask import session
        from app.models.user import User

        user = None
        user_id = session.get("user_id")
        if user_id is not None:
            try:
                # User model uses integer IDs in SQLite
                user = User.get_by_id(int(user_id))
            except Exception:
                user = None

        return dict(current_user=user)

    # Register 404 error handler
    @app.errorhandler(404)
    def page_not_found(e):
        """Handle 404 errors with custom template"""
        from flask import render_template
        return render_template('404.html'), 404

    return app