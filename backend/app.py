from flask_cors import CORS
from flask import Flask
from werkzeug.security import generate_password_hash
from config import LocalDevelopmentConfig
from models import db, User 
from security import jwt
import os
from celery_init import celery_init_app
from celery.schedules import crontab
from cache import cache

app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    CORS(app)
    db.init_app(app)
    app.config['JWT_SECRET_KEY'] = 'this-is-a-super-secret-key-12345'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads', 'resumes')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True) 
    OFFER_FOLDER = os.path.join(os.getcwd(), 'offer_letters')
    os.makedirs(OFFER_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['OFFER_FOLDER'] = OFFER_FOLDER   
    jwt.init_app(app)
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_URL'] = 'redis://127.0.0.1:6379/1'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300 # Default expiry: 5 minute
    cache.init_app(app)
    app.app_context().push()
    return app

app = create_app()
celery = celery_init_app(app)
celery.autodiscover_tasks()

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

celery.conf.beat_schedule = {
    'auto-close-expired-drives': {
        'task': 'close_expired_drives',
        'schedule': crontab(hour=0, minute=0), 
    },
    'daily-interview-reminders': {
        'task': 'send_daily_interview_reminders', 
        'schedule': crontab(hour=8, minute=0), 
    },
    'monthly-company-reports': {
        'task': 'generate_monthly_company_reports',
        'schedule': crontab(minute=0, hour=0, day_of_month='1'),
    },
    'admin-monthly-report': {
        'task': 'generate_admin_monthly_report',
        'schedule': crontab(minute=0, hour=0, day_of_month='1'),
    },
    'daily-deadline-notifications': {
        'task': 'send_daily_deadline_reminders',
        'schedule': crontab(hour=8, minute=0),
    },
}

if __name__ == '__main__':
    create_database() 
    app.run(debug=True, port=5000)