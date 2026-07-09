import requests
from celery import shared_task
import csv
import os
from datetime import datetime
from models import  Application, PlacementDrive, CompanyProfile, StudentProfile, db
from mail import send_email
from datetime import timedelta, datetime
from flask import render_template

@shared_task(ignore_result=False, name="export_student_csv")
def export_student_applications(student_id):
    EXPORT_FOLDER = os.path.join(os.getcwd(), 'static', 'exports')
    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"applications_student_{student_id}_{timestamp}.csv"
    filepath = os.path.join(EXPORT_FOLDER, filename)
    applications = Application.query.filter_by(student_id=student_id).all()

    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Student ID', 'Company Name', 'Drive Title', 'Application Status', 'Date Applied', 'Interview Date'])        
        for app in applications:
            drive = PlacementDrive.query.get(app.drive_id)
            company = CompanyProfile.query.get(drive.company_id) if drive else None
            
            company_name = company.name if company else "Unknown"
            drive_title = drive.job_title if drive else "Unknown"
            date_applied = app.date_applied.strftime("%Y-%m-%d")
            interview_date = app.interview_date if app.interview_date else "N/A"
            writer.writerow([student_id, company_name, drive_title, app.status, date_applied, interview_date])
    student_profile = StudentProfile.query.get(student_id)
    
    if student_profile:
        text = f"Hello {student_profile.full_name}, your asynchronous batch job is complete. Your CSV export has been downloaded"
        response = requests.post("https://chat.googleapis.com/v1/spaces/AAQAS3vnmXg/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=IuLvBST9hVIYdB-5OtIbgo4uwi-RoY1_kahPKn_i6hA", json = {"text": text})
        print(response.status_code)
    return filename

@shared_task(ignore_result=True, name="send_daily_interview_reminders")
def send_interview_reminders():
    tomorrow = datetime.now().date() + timedelta(days=1)
    upcoming_interviews = Application.query.filter(Application.interview_date == tomorrow).all()
    reminders_sent = 0
    for app in upcoming_interviews:
        student = StudentProfile.query.get(app.student_id)
        if not student:
            print(f"DEBUG: Skipped Application {app.id} - No StudentProfile found.")
            continue
            
        drive = PlacementDrive.query.get(app.drive_id)
        company_name = "the company"
        if drive:
            company = CompanyProfile.query.get(drive.company_id)
            if company:
                company_name = company.name
        
        subject = f"Reminder: Upcoming Interview with {company_name}"
        body = f"<p>Hello {student.full_name}, this is a reminder for your interview tomorrow with {company_name}.</p>"
        
        if send_email(to=student.email, subject=subject, body=body):
            reminders_sent += 1
            print(f"Email successfully sent to {student.email}")
    return f"Job Complete: Sent {reminders_sent} interview reminders."


@shared_task(ignore_result=True, name="generate_monthly_company_reports")
def generate_monthly_reports():
    current_month = datetime.now().strftime("%B %Y")
    companies = CompanyProfile.query.filter_by(is_approved=True).all()
    reports_sent = 0
    
    for company in companies:
        if not company or not company.email:
            continue
        drives = PlacementDrive.query.filter_by(company_id=company.id).all()
        drive_ids = [drive.id for drive in drives]
        if not drive_ids:
            continue
        total_apps = Application.query.filter(Application.drive_id.in_(drive_ids)).count()
        accepted = Application.query.filter(Application.drive_id.in_(drive_ids), Application.status == 'Accepted').count()
        shortlisted = Application.query.filter(Application.drive_id.in_(drive_ids), Application.status == 'Shortlisted').count()
        rejected = Application.query.filter(Application.drive_id.in_(drive_ids), Application.status == 'Rejected').count()
        
        html_body = render_template(
            'monthly_report.html',
            month_name=current_month,
            company_name=company.name,
            total_apps=total_apps,
            accepted=accepted,
            shortlisted=shortlisted,
            rejected=rejected
        )
        subject = f"Your Monthly Placement Analytics - {current_month}"
        if send_email(to=company.email, subject=subject, body=html_body):
            reports_sent += 1
            print(f"Monthly report sent to {company.name} ({company.email})")
    return f"Job Complete: Sent {reports_sent} monthly reports."

@shared_task(ignore_result=False, name="export_company_csv")
def export_company_applications(company_id):
    EXPORT_FOLDER = os.path.join(os.getcwd(), 'static', 'exports')
    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"applications_company_{company_id}_{timestamp}.csv"
    filepath = os.path.join(EXPORT_FOLDER, filename)
    
    company = CompanyProfile.query.get(company_id)
    if not company:
        return None
    drives = PlacementDrive.query.filter_by(company_id=company.id).all()
    drive_ids = [drive.id for drive in drives]
    applications = Application.query.filter(Application.drive_id.in_(drive_ids)).all()
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Student Name', 'Job Title', 'Application Status', 'Date Applied', 'Interview Date'])      
        for app in applications:
            student = StudentProfile.query.get(app.student_id)
            drive = PlacementDrive.query.get(app.drive_id)
            student_name = student.full_name if student else "Unknown"
            job_title = drive.job_title if drive else "Unknown"
            
            date_applied = app.date_applied.strftime("%Y-%m-%d") if app.date_applied else "N/A"
            interview_date = app.interview_date.strftime("%Y-%m-%d") if app.interview_date else "N/A"
            writer.writerow([student_name, job_title, app.status, date_applied, interview_date])

    if company :
        text = f"Hello {company.name}, your asynchronous CSV batch job is complete. Your candidate export is ready to download from your dashboard!"
        response = requests.post("https://chat.googleapis.com/v1/spaces/AAQAS3vnmXg/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=IuLvBST9hVIYdB-5OtIbgo4uwi-RoY1_kahPKn_i6hA", json = {"text": text})
        print(response.status_code)
    return filename

@shared_task(ignore_result=True, name="generate_admin_monthly_report")
def generate_admin_report():
    current_month = datetime.now().strftime("%B %Y")
    email = "admin123@gmail.com"
    total_drives = PlacementDrive.query.count()
    total_apps = Application.query.count()
    total_selected = Application.query.filter_by(status='Accepted').count() 
    
    html_body = render_template(
        'admin_monthly_report.html',
        month_name=current_month,
        total_drives=total_drives,
        total_apps=total_apps,
        total_selected=total_selected
    )
    subject = f"Institute Placement Report - {current_month}"
    if send_email(to=email, subject=subject, body=html_body):
        print("Admin monthly report sent successfully ")
        return "Job Complete: Admin report sent."
    return "Failed to send email."

@shared_task(ignore_result=True, name="send_daily_deadline_reminders")
def check_upcoming_deadlines():
    tomorrow = datetime.now().date() + timedelta(days=1)
    closing_drives = PlacementDrive.query.filter(
        db.func.date(PlacementDrive.deadline) == tomorrow
    ).all()
    if not closing_drives:
        print(f"DEBUG: No placement application deadlines closing on {tomorrow}.")
        return "Job Complete: 0 deadlines found."
    message_header = f"🚨 *DAILY PLACEMENT DEADLINE ALERTS - CLOSING TOMORROW ({tomorrow})* 🚨\n\n"
    drive_listings = ""
    for drive in closing_drives:
        company = CompanyProfile.query.get(drive.company_id)
        company_name = company.name if company else "Unknown Company"
        salary_info = drive.salary if drive.salary else "Not disclosed"
        skills_info = drive.required_skills if drive.required_skills else "Check portal for details"
        cgpa_info = f"{drive.min_cgpa}+" if drive.min_cgpa > 0 else "No strict cutoff"
        drive_listings += f"🏢 *{drive.job_title}* at _{company_name}_\n"
        drive_listings += f"  💰 *Salary:* {salary_info}\n"
        drive_listings += f"  🎓 *Eligibility:* {drive.branch} | CGPA: {cgpa_info}\n"
        drive_listings += f"  🛠️ *Skills:* {skills_info}\n"
        drive_listings += f"  👉 _Apply via your student portal before midnight!_\n\n"
    text = message_header + drive_listings
    response = requests.post("https://chat.googleapis.com/v1/spaces/AAQAS3vnmXg/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=IuLvBST9hVIYdB-5OtIbgo4uwi-RoY1_kahPKn_i6hA", json = {"text": text})
    print(response.status_code)
    return f"Job Complete: Dispatched {len(closing_drives)} alerts."
    
@shared_task(ignore_result=True, name="close_expired_drives")
def auto_close_drives():
    current_time = datetime.now()
    expired_drives = PlacementDrive.query.filter(
        PlacementDrive.deadline < current_time,
        PlacementDrive.status != 'Closed'
    ).all()
    if not expired_drives:
        return "Job Complete: No new expired drives to close."
    closed_count = 0
    for drive in expired_drives:
        drive.status = 'Closed' 
        closed_count += 1
    db.session.commit()
    return f"Job Complete: Closed {closed_count} drives."
