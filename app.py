import os
from flask import Flask
from models import db
from dotenv import load_dotenv
load_dotenv()

def create_app(test_config=None):
    
    #import blueprints
    from main import main
    from auth import auth


    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI = "sqlite:///posts.sqlite3",
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SECRET_KEY = os.getenv("SECRET_KEY")
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #initialize database
    db.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(auth)
    with app.app_context():

        db.create_all()
        app.run(debug=True)

    return app
