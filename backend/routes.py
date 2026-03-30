from flask import current_app as app, jsonify, request, abort
from models import User, db, StudentProfile, CompanyProfile
from flask_jwt_extended import create_access_token, current_user, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps



def role_required(required_role):
    def wrapper (fn):
        @jwt_required()
        @wraps(fn)
        def decorator(*args, **kwargs):
            if current_user.role != required_role:
                return jsonify (message = "You are not authorized"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@app.route('/')
def index():
    return {"message": "Placement Portal API is running!"}

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    if not username or not password or not role:
        return jsonify({"message": "Missing required fields"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 409
    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password=hashed_pw, role=role)
    db.session.add(new_user)
    db.session.commit() 

    if role == 'student':
        profile = StudentProfile(user_id=new_user.id, full_name=data.get('full_name', 'Update Name'), cgpa=0.0)
        db.session.add(profile)
    elif role == 'company':
        profile = CompanyProfile(user_id=new_user.id, name=data.get('company_name', 'Update Company Name'))
        db.session.add(profile)
    
    db.session.commit()
    return jsonify({"message": f"{role.capitalize()} registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401
    access_token = create_access_token(identity=user)
    return jsonify(access_token = access_token, role=user.role), 200

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password) or user.role != 'admin':
        return jsonify({"message": "Invalid admin credentials"}), 401

    access_token = create_access_token(identity=user)

    return jsonify({
        "message": "Admin login successful",
        "access_token": access_token,
        "role": user.role
    }), 200

# *===============**===============**===============**===============**===============**===============**===============*
# ||   ADMIN     ||||   ADMIN     ||||   ADMIN     ||||   ADMIN     ||||   ADMIN     ||||   ADMIN     ||||   ADMIN     ||
# *===============**===============**===============**===============**===============**===============**===============*
@app.route('/api/admin-dashboard', methods=['GET'])
@role_required("admin")
def admin_dashboard():
    return jsonify({"message": "Welcome to the Admin Dashboard API!"}), 200


# *===============**===============**===============**===============**===============**===============**===============*
# ||   STUDENT   ||||   STUDENT   ||||   STUDENT   ||||   STUDENT   ||||   STUDENT   ||||   STUDENT   ||||   STUDENT   ||
# *===============**===============**===============**===============**===============**===============**===============*
@app.route('/api/student-dashboard', methods=['GET'])
@role_required("student")
def student_dashboard():
    return jsonify({"message": "Welcome to the Student Dashboard API!"}), 200


# *===============**===============**===============**===============**===============**===============**===============*
# ||   COMPANY   ||||   COMPANY   ||||   COMPANY   ||||   COMPANY   ||||   COMPANY   ||||   COMPANY   ||||   COMPANY   ||
# *===============**===============**===============**===============**===============**===============**===============*
@app.route('/api/company-dashboard', methods=['GET'])
@role_required("company")
def company_dashboard():
    return jsonify({"message": "Welcome to the company Dashboard API!"}), 200





