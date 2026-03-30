from flask_cors import CORS
from flask import Flask
from werkzeug.security import generate_password_hash
from config import LocalDevelopmentConfig
from models import db, User, CompanyProfile, StudentProfile 
from security import jwt, JWTManager

app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    CORS(app)
    db.init_app(app)
    app.config['JWT_SECRET_KEY'] = 'this-is-a-super-secret-key-12345'
    jwt.init_app(app)
    app.app_context().push()
    return app

app = create_app()

from routes import *

def create_database():
    with app.app_context():
        db.create_all()
        
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            print("No Admin found. Creating default admin...")
            new_admin = User(
                username='admin', 
                password=generate_password_hash('admin123'), 
                role='admin'
            )
            student = User(username='student',password=generate_password_hash('student123'),)
            company = User(username='company',password=generate_password_hash('company123'),role='company')
            db.session.add_all([new_admin, student, company])
            db.session.commit()
            print("Admin 'admin' created successfully.")
        else:
            print("Admin already exists. Skipping creation.")



if __name__ == '__main__':
    create_database() 
    app.run(debug=True, port=5000)