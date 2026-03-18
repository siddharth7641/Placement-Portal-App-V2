import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from models import db, User, CompanyProfile, StudentProfile # Importing from our models file

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join( 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_super_secret_key_here' # Needed for JWT/Sessions later

db.init_app(app)

def create_database():
    with app.app_context():
        db.create_all()
        
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            print("No Admin found. Creating default admin...")
            hashed_pw = generate_password_hash('admin123') # Default password
            new_admin = User(
                username='admin@institute.edu', 
                password=hashed_pw, 
                role='admin'
            )
            db.session.add(new_admin)
            db.session.commit()
            print("Admin 'admin@institute.edu' created successfully.")
        else:
            print("Admin already exists. Skipping creation.")

@app.route('/')
def index():
    return {"message": "Placement Portal API is running!"}

if __name__ == '__main__':
    create_database() 
    app.run(debug=True, port=5000)