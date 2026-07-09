from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default = 'student', nullable = False)
    is_blacklisted = db.Column(db.Boolean, default=False)
    student_profile = db.relationship('StudentProfile', backref='user', uselist=False)
    company_profile = db.relationship('CompanyProfile', backref='user', uselist=False)

class CompanyProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(100))
    is_approved = db.Column(db.Boolean, default=False)
    drives = db.relationship('PlacementDrive', backref='company', lazy=True)
    about_us = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(15), nullable=True)

class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    branch = db.Column(db.String(50))
    resume_path = db.Column(db.String(200))
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    skills = db.Column(db.String(255), nullable=True)
    experience = db.Column(db.Text, nullable=True)

class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profile.id'), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text)
    branch = db.Column(db.String(100), nullable=False)
    min_cgpa = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='Pending')
    applications = db.relationship('Application', backref='drive', lazy=True)
    required_skills = db.Column(db.String(255), nullable=True)
    experience_required = db.Column(db.String(100), nullable=True)
    salary = db.Column(db.String(100), nullable=True)
    benefits = db.Column(db.Text, nullable=True)
    deadline = db.Column(db.DateTime, nullable=True)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'), nullable=False)
    status = db.Column(db.String(20), default='Applied')
    date_applied = db.Column(db.DateTime, default=datetime.utcnow)
    interview_date = db.Column(db.Date, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    offer_letter_path = db.Column(db.String(255), nullable=True)