from flask import current_app as app, jsonify, request, abort
from models import User, db, StudentProfile, CompanyProfile, Application, PlacementDrive    
from flask_jwt_extended import create_access_token, current_user, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory

# *===============**=====
# ||   decorator     ||||
# *===============**=====
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


# *===============**===============**===============**===============**===============**===============**===============*
# ||   universal     ||||   universal     ||||   universal     ||||   universal     ||||   universal     ||||   universal          ||
# *===============**===============**===============**===============**===============**===============**===============*
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
    if user and check_password_hash(user.password, password):
        if user.is_blacklisted:
            return jsonify({"message": "Your account has been suspended by the Admin."}), 403
        elif user.role == 'company':
            company_profile = CompanyProfile.query.filter_by(user_id=user.id).first()
            if not company_profile.is_approved:
                return jsonify({"message": "Your company account is not approved yet."}), 403

        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token, role=user.role), 200

    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/api/download-resume/<filename>', methods=['GET'])
@jwt_required() # Works for admin, company, or student!
def download_resume(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return jsonify({"message": "File not found."}), 404
    
@app.route('/api/download-offer/<filename>', methods=['GET'])
def download_offer(filename):
    import os
    from flask import send_from_directory
    
    # 2. DEFINE THE FOLDER HERE TOO
    OFFER_FOLDER = os.path.join(os.getcwd(), 'offer_letters')
    
    return send_from_directory(OFFER_FOLDER, filename)
    
# *===============**===============**===============**===============**===============**===============**===============*
# ||   ADMIN     ||||   ADMIN     ||||   ADMIN     ||||   ADMIN     ||||   ADMIN     ||||   ADMIN     ||||   ADMIN     ||
# *===============**===============**===============**===============**===============**===============**===============*
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

@app.route('/api/admin/dashboard', methods=['GET'])
@role_required('admin')
def admin_dashboard_stats():
    all_companies = CompanyProfile.query.all()
    active_comps = []
    banned_comps = []
    for c in all_companies:
        user_acct = User.query.get(c.user_id)
        comp_data = {"id": c.id, "name": c.name, "email": c.email, "phone": c.phone}
        if user_acct.is_blacklisted:
            banned_comps.append(comp_data)
        elif c.is_approved:
            active_comps.append(comp_data)
    all_students = StudentProfile.query.all()
    active_stus = []
    banned_stus = []
    for s in all_students:
        user_acct = User.query.get(s.user_id)
        stu_data = {"id": s.id, "name": s.full_name, "email": s.email, "phone": s.phone}
        if user_acct.is_blacklisted:
            banned_stus.append(stu_data)
        else:
            active_stus.append(stu_data)
    applications = Application.query.all()
    app_list = []
    for app in applications:
        student = StudentProfile.query.get(app.student_id)
        drive = PlacementDrive.query.get(app.drive_id)
        company = CompanyProfile.query.get(drive.company_id) if drive else None
        app_list.append({
            "id": app.id,
            "studentName": student.full_name if student else "Unknown",
            "driveName": drive.job_title if drive else "Unknown",
            "companyName": company.name if company else "Unknown",
            "date": app.date_applied.strftime("%d/%m/%Y"),
            "resume_path": student.resume_path if student else None
        })
    drives = PlacementDrive.query.filter_by(status='Approved').all()
    ongoing_drive_list = []
    for d in drives:
        ongoing_drive_list.append({
            "id": d.id, 
            "name": d.job_title, 
            "company": d.company.name,
            "status": d.status,
            "branch": d.branch,
            "min_cgpa": d.min_cgpa,
            "description": d.job_description
        })
    closed_drives = PlacementDrive.query.filter_by(status='Closed').all()
    closed_drive_list = []
    for d in closed_drives:
        closed_drive_list.append({
            "id": d.id, 
            "name": d.job_title, 
            "company": d.company.name,
            "status": d.status,
            "branch": d.branch,
            "min_cgpa": d.min_cgpa,
            "description": d.job_description
        })
    pending_drives = PlacementDrive.query.filter_by(status='Pending').all()
    pending_drive_list = []
    for d in pending_drives:
        pending_drive_list.append({
            "id": d.id, 
            "name": d.job_title, 
            "company": d.company.name,
            "status": d.status,
            "branch": d.branch,
            "min_cgpa": d.min_cgpa,
            "description": d.job_description
        })
    rejected_drives = PlacementDrive.query.filter_by(status='Rejected').all()
    rejected_drive_list = []
    for d in rejected_drives:
        rejected_drive_list.append({
            "id": d.id,
            "name": d.job_title,
            "company": d.company.name,
            "status": d.status,
            "branch": d.branch,
            "min_cgpa": d.min_cgpa,
            "description": d.job_description
        })
    return jsonify({
        "registeredCompanies": active_comps,
        "blacklistedCompanies": banned_comps,
        "registeredStudents": active_stus,
        "blacklistedStudents": banned_stus,
        "ongoingDrives": ongoing_drive_list,
        "closedDrives": closed_drive_list, 
        "studentApplications": app_list,
        "pendingDrives": pending_drive_list,
        "rejectedDrives": rejected_drive_list
    }), 200

@app.route('/api/admin/pending-companies', methods=['GET'])
@role_required('admin') 
def get_pending_companies():
    pending_companies = CompanyProfile.query.filter_by(is_approved=False).all()
    result = []
    for company in pending_companies:
        result.append({
            "id": company.id,
            "name": company.name,
            "username": company.user.username 
        })
    return jsonify(result), 200

@app.route('/api/admin/company-action/<int:company_id>', methods=['POST'])
@role_required('admin')
def company_action(company_id):
    data = request.get_json()
    action = data.get('action') 
    company = CompanyProfile.query.get_or_404(company_id)
    user_account = User.query.get(company.user_id)
    if action == 'approve':
        company.is_approved = True
        user_account.is_blacklisted = False
        db.session.commit()
        return jsonify({"message": f"{company.name} approved!"}), 200
    elif action == 'reject':
        user = User.query.get(company.user_id)
        db.session.delete(company)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Company rejected and deleted."}), 200
    elif action == 'blacklist':
        company.is_approved = True
        user_account.is_blacklisted = True
        drives = PlacementDrive.query.filter_by(company_id=company.id).all()
        for drive in drives:
            drive.status = 'Cancelled'
        db.session.commit()
        return jsonify({"message": f"{company.name} suspended."}), 200
    elif action == 'unblacklist':
        user_account.is_blacklisted = False
        company.is_approved = True
        drives = PlacementDrive.query.filter_by(company_id=company.id).all()
        for drive in drives:
            drive.status = 'Approved'
        db.session.commit()
        return jsonify({"message": f"{company.name} reinstated!"}), 200
    return jsonify({"message": "Invalid action"}), 400

@app.route('/api/admin/drive-action/<int:drive_id>', methods=['POST'])
@role_required('admin')
def admin_drive_action(drive_id):
    action = request.json.get('action')
    if action not in ['approve', 'reject']:
        return jsonify({"message": "Invalid action"}), 400
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({"message": "Placement drive not found."}), 404
    if action == 'approve':
        drive.status = 'Approved'
        message = f"Drive '{drive.job_title}' has been officially approved."
    elif action == 'reject':
        drive.status = 'Rejected'
        message = f"Drive '{drive.job_title}' has been rejected."
    db.session.commit()
    return jsonify({"message": message}), 200

@app.route('/api/admin/student-action/<int:student_id>', methods=['POST'])
@role_required('admin')
def student_action(student_id):
    data = request.get_json()
    action = data.get('action')
    student = StudentProfile.query.get_or_404(student_id)
    user_account = User.query.get(student.user_id)
    if action == 'blacklist':
        user_account.is_blacklisted = True
        db.session.commit()
        return jsonify({"message": "Student suspended."}), 200
    elif action == 'unblacklist':
        user_account.is_blacklisted = False
        db.session.commit()
        return jsonify({"message": "Student reinstated."}), 200
    return jsonify({"message": "Invalid action"}), 400

@app.route('/api/admin/drive/<int:drive_id>/close', methods=['POST'])
@role_required('admin')
def admin_close_drive(drive_id):
    drive = PlacementDrive.query.filter_by(id=drive_id).first()
    if not drive:
        return jsonify({"message": "Drive not found or unauthorized."}), 404
    drive.status = 'Closed'
    db.session.commit()
    return jsonify({"message": "Drive officially closed!"}), 200

# *===============**===============**===============**===============**===============**===============**===============*
# ||   COMPANY   ||||   COMPANY   ||||   COMPANY   ||||   COMPANY   ||||   COMPANY   ||||   COMPANY   ||||   COMPANY   ||
# *===============**===============**===============**===============**===============**===============**===============*

@app.route('/api/company/dashboard', methods=['GET'])
@role_required('company')
def company_dashboard():
    company = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    if not company:
        return jsonify({"message": "Company profile not found."}), 404
    drives = PlacementDrive.query.filter_by(company_id=company.id).all()
    upcoming_drives = []
    closed_drives = []
    for drive in drives:
        drive_data = {
            "id": drive.id,
            "name": drive.job_title,
            "status": drive.status,
            "applicantCount": len(drive.applications) 
        }
        if drive.status == 'Closed':
            closed_drives.append(drive_data)
        else:
            upcoming_drives.append(drive_data)
    return jsonify({
        "companyName": company.name,
        "upcomingDrives": upcoming_drives,
        "aboutUs": company.about_us,
        "website": company.website,
        "closedDrives": closed_drives
    }), 200

@app.route('/api/company/profile', methods=['PUT'])
@role_required('company')
def update_company_profile():
    company = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    data = request.get_json()
    if 'name' in data:
        company.name = data['name']
    if 'about_us' in data:
        company.about_us = data['about_us']
    if 'website' in data:
        company.website = data['website']
    db.session.commit()
    return jsonify({"message": "Company profile updated successfully!"}), 200

@app.route('/api/company/post-drive', methods=['POST'])
@role_required('company')
def post_new_drive():
    company = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    if not company:
        return jsonify({"message": "Company profile not found."}), 404
    data = request.json
    new_drive = PlacementDrive(
        company_id=company.id,
        job_title=data.get('job_title'),
        job_description=data.get('job_description'),
        branch=data.get('branch'),
        min_cgpa=float(data.get('min_cgpa', 0.0)),
        required_skills=data.get('required_skills'),
        experience_required=data.get('experience_required'),
        salary=data.get('salary'),
        benefits=data.get('benefits')
    )
    db.session.add(new_drive)
    db.session.commit()
    return jsonify({"message": "Job posted successfully! Pending Admin approval."}), 201

@app.route('/api/company/drive/<int:drive_id>/applicants', methods=['GET'])
@role_required('company')
def get_drive_applicants(drive_id):
    company = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    drive = PlacementDrive.query.filter_by(id=drive_id, company_id=company.id).first()
    if not drive:
        return jsonify({"message": "Drive not found or unauthorized."}), 404
    applications = Application.query.filter_by(drive_id=drive.id).all()
    applicant_list = []
    for app in applications:
        student = StudentProfile.query.get(app.student_id)
        applicant_list.append({
            "application_id": app.id,
            "student_name": student.full_name,
            "cgpa": student.cgpa,
            "branch": student.branch,
            "skills": student.skills,
            "experience": student.experience,
            "resume_path": student.resume_path,
            "status": app.status,
            "date_applied": app.date_applied.strftime("%d/%m/%Y"),
            "interview_date": app.interview_date,
            "feedback": app.feedback
        })
    return jsonify({
        "drive_name": drive.job_title,
        "applicants": applicant_list
    }), 200

@app.route('/api/company/application/<int:app_id>/update', methods=['PUT'])
@role_required('company')
def update_application_status(app_id):
    application = Application.query.get(app_id)
    if not application:
        return jsonify({"message": "Application not found."}), 404
    company = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    drive = PlacementDrive.query.get(application.drive_id)
    if drive.company_id != company.id:
        return jsonify({"message": "Unauthorized access."}), 403
    data = request.json
    if 'status' in data:
        application.status = data['status']
    if 'feedback' in data:
        application.feedback = data['feedback']
    if 'interview_date' in data:
        application.interview_date = data['interview_date']
    db.session.commit()
    return jsonify({"message": f"Student marked as {application.status} successfully."}), 200

@app.route('/api/company/drive/<int:drive_id>/close', methods=['POST'])
@role_required('company')
def close_drive(drive_id):
    company = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    drive = PlacementDrive.query.filter_by(id=drive_id, company_id=company.id).first()
    if not drive:
        return jsonify({"message": "Drive not found or unauthorized."}), 404
    drive.status = 'Closed'
    db.session.commit()
    return jsonify({"message": "Drive officially closed!"}), 200

@app.route('/api/company/application/<int:app_id>/upload-offer', methods=['POST'])
@role_required('company')
def upload_offer_letter(app_id):
    import os
    from werkzeug.utils import secure_filename
    OFFER_FOLDER = os.path.join(os.getcwd(), 'offer_letters')
    os.makedirs(OFFER_FOLDER, exist_ok=True)
    application = Application.query.get(app_id)
    if not application:
        return jsonify({"message": "Application not found"}), 404
    if 'offer_letter' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['offer_letter']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        unique_filename = f"app_{app_id}_{filename}"
        file.save(os.path.join(OFFER_FOLDER, unique_filename))
        application.offer_letter_path = unique_filename
        db.session.commit()
        return jsonify({"message": "Offer letter uploaded successfully!", "path": unique_filename}), 200

# *===============**===============**===============**===============**===============**===============**===============*
# ||   STUDENT   ||||   STUDENT   ||||   STUDENT   ||||   STUDENT   ||||   STUDENT   ||||   STUDENT   ||||   STUDENT   ||
# *===============**===============**===============**===============**===============**===============**===============*

@app.route('/api/student/dashboard', methods=['GET'])
@role_required('student')
def student_dashboard():
    student = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not student:
        return jsonify({"message": "Student profile not found."}), 404
    companies = CompanyProfile.query.filter_by(is_approved=True).all()
    org_list = [{"id": c.id, "name": c.name} for c in companies]
    active_drives = PlacementDrive.query.filter_by(status='Approved').all()
    available_drives = []
    for d in active_drives:
        comp = CompanyProfile.query.get(d.company_id)
        available_drives.append({
            "id": d.id,
            "job_title": d.job_title,
            "company_name": comp.name if comp else "Unknown",
            "branch": d.branch,
            "min_cgpa": d.min_cgpa,
            "description": d.job_description,
            "skills" : d.required_skills,
        })
    my_apps = Application.query.filter_by(student_id=student.id).all()
    applied_list = []
    for app in my_apps:
        drive = PlacementDrive.query.get(app.drive_id)
        company = CompanyProfile.query.get(drive.company_id) if drive else None
        applied_list.append({
            "id": app.id,
            "drive_id": drive.id,
            "drive_name": drive.job_title,
            "company_name": company.name if company else "Unknown",
            "date": app.date_applied.strftime("%d/%m/%Y"),
            "status": app.status,
            "interview_date": app.interview_date,
            "feedback": app.feedback,
            "offer_letter_path": app.offer_letter_path
        })
    return jsonify({
        "studentName": student.full_name,
        "email": student.email,
        "phone": student.phone,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "resume_path": student.resume_path,
        "skills": student.skills, 
        "experience": student.experience,
        "organizations": org_list,
        "availableDrives": available_drives,
        "appliedDrives": applied_list
    }), 200

@app.route('/api/student/company/<int:company_id>', methods=['GET'])
@role_required('student')
def student_company_details(company_id):
    company = CompanyProfile.query.get_or_404(company_id)
    drives = PlacementDrive.query.filter_by(company_id=company.id, status='Approved').all()
    student = StudentProfile.query.filter_by(user_id=current_user.id).first()
    applied_drive_ids = [app.drive_id for app in Application.query.filter_by(student_id=student.id).all()]
    drive_list = [{
        "id": d.id,
        "job_title": d.job_title,
        "job_description": d.job_description,
        "has_applied": d.id in applied_drive_ids
    } for d in drives]
    return jsonify({
        "id": company.id,
        "name": company.name,
        "overview": company.about_us or "No company overview provided yet.",
        "website": company.website,
        "drives": drive_list,
    }), 200

@app.route('/api/student/history', methods=['GET'])
@role_required('student')
def student_history():
    student = StudentProfile.query.filter_by(user_id=current_user.id).first()
    applications = Application.query.filter_by(student_id=student.id).all()
    history_list = []
    for app in applications:
        drive = PlacementDrive.query.get(app.drive_id)
        history_list.append({
            "drive_no": drive.id,
            "interview": "In-person",
            "job_title": drive.job_title,
            "results": app.status,
            "remark": "None"
        })
    return jsonify(history_list), 200

@app.route('/api/student/apply/<int:drive_id>', methods=['POST'])
@role_required('student')
def apply_for_job(drive_id):
    student = StudentProfile.query.filter_by(user_id=current_user.id).first()
    drive = PlacementDrive.query.get(drive_id)
    if not student or not drive:
        return jsonify({"message": "Invalid request."}), 404
    existing_application = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first()
    if existing_application:
        return jsonify({"message": "You have already applied for this position."}), 400
    if student.cgpa < drive.min_cgpa:
        return jsonify({"message": "Your CGPA does not meet the minimum requirement for this drive."}), 400
    new_application = Application(
        student_id=student.id,
        drive_id=drive_id,
        status='Applied'
    )
    db.session.add(new_application)
    db.session.commit()
    return jsonify({"message": "Successfully applied for the job!"}), 201

@app.route('/api/student/profile', methods=['PUT'])
@role_required('student')
def update_student_profile():
    student = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not student:
        return jsonify({"message": "Profile not found"}), 404
    data = request.get_json()
    if 'full_name' in data:
        student.full_name = data['full_name']
    if 'branch' in data:
        student.branch = data['branch']
    if 'cgpa' in data:
        student.cgpa = float(data['cgpa'])
    if 'skills' in data: 
        student.skills = data['skills']
    if 'experience' in data: 
        student.experience = data['experience']
    db.session.commit()
    return jsonify({"message": "Profile updated successfully!"}), 200

@app.route('/api/student/upload-resume', methods=['POST'])
@role_required('student')
def upload_resume():
    student = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if 'resume' not in request.files:
        return jsonify({"message": "No file part found"}), 400
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"message": "Only PDF files are allowed!"}), 400
    filename = secure_filename(f"student_{student.id}_{file.filename}")
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)
    student.resume_path = filename
    db.session.commit()
    return jsonify({"message": "Resume uploaded successfully!", "filename": filename}), 200