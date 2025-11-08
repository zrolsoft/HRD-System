from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes import employees, departments
    app.register_blueprint(employees.bp)
    app.register_blueprint(departments.bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
