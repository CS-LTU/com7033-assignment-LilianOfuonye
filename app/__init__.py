from flask import Flask


# This is where the flask app will be created.would function as a central point to hold everything together. 
def create_app():
    app = Flask(__name__)
    from app.routes import auth
    app.register_blueprint(auth.auth_blueprint)


    return app