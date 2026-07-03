<template>
  <div class="container mt-4 mb-5">
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
      <h4 class="mb-0 text-dark">Welcome, {{ companyName }}</h4>
      <button v-if="!currentView" @click="currentView = 'postJob'" class="btn btn-primary rounded-pill px-4 shadow-sm">
        <i class="fa-solid fa-plus me-2"></i> Post a New Job
      </button>
    </div>

    <div v-if="!currentView">
      <div class="card shadow-sm border-0 mb-5 bg-light">
        <div class="card-body p-4">
          <div class="row">
            <div class="col-md-8">
              
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="text-secondary mb-0"><i class="fa-solid fa-building me-2"></i>Company Overview</h5>
                <button v-if="!isEditingProfile" @click="startEditing" class="btn btn-sm btn-outline-primary rounded-pill px-3">
                  <i class="fa-solid fa-pen me-1"></i> Edit
                </button>
                <div v-else class="d-flex gap-2">
                  <button @click="saveProfile" class="btn btn-sm btn-success rounded-pill px-3">Save</button>
                  <button @click="isEditingProfile = false" class="btn btn-sm btn-outline-secondary rounded-pill px-3">Cancel</button>
                </div>
              </div>

              <div v-if="!isEditingProfile">
                <p v-if="website" class="mb-2">
                  <i class="fa-solid fa-globe me-2 text-primary"></i>
                  <a :href="website" target="_blank" class="text-decoration-none">{{ website }}</a>
                </p>
                <p v-else class="text-muted small mb-2"><i class="fa-solid fa-link me-1"></i>No website added</p>
                <p class="text-dark small lh-lg mb-4" style="white-space: pre-line;">{{ aboutUs || "No overview provided yet." }}</p>
              </div>

              <div v-else class="mb-4 bg-white p-3 rounded border">
                <div class="mb-2">
                  <label class="form-label text-secondary fw-semibold small mb-1">Company Name</label>
                  <input type="text" class="form-control form-control-sm" v-model="editForm.name" placeholder="Enter company name">
                </div>
                <div class="mb-2">
                  <label class="form-label text-secondary fw-semibold small mb-1">Website URL</label>
                  <input type="url" class="form-control form-control-sm" v-model="editForm.website" placeholder="https://www.example.com">
                </div>
                <div class="mb-2">
                  <label class="form-label text-secondary fw-semibold small mb-1">About Us</label>
                  <textarea class="form-control form-control-sm" v-model="editForm.about_us" rows="4" placeholder="Tell students about your company..."></textarea>
                </div>
                <div class="mb-2">
                  <label class="form-label text-secondary fw-semibold small mb-1">Email</label>
                  <input type="email" class="form-control form-control-sm" v-model="editForm.email" placeholder="Enter company email">
                </div>
              </div>

              <button 
                @click="exportHistory" 
                class="btn btn-sm btn-outline-success rounded-pill px-4 shadow-sm"
                :disabled="isExporting || isEditingProfile"
                >
                <span v-if="isExporting"><i class="fa-solid fa-spinner fa-spin me-2"></i> Generating CSV...</span>
                <span v-else><i class="fa-solid fa-file-csv me-1"></i> Export History</span>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="mb-5">
        <h5 class="text-secondary mb-3"><i class="fa-solid fa-briefcase me-2"></i>Active Job Postings ({{ upcomingDrives.length }})</h5>
        <div class="table-responsive border rounded bg-white shadow-sm">
          <table class="table table-hover mb-0 align-middle">
            <thead class="table-light">
              <tr>
                <th class="ps-3">Role</th>
                <th>Status</th>
                <th>Applicants</th>
                <th class="text-end pe-4">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="upcomingDrives.length === 0">
                <td colspan="4" class="text-center text-muted py-4">No active job postings. Click "Post a New Job" to get started.</td>
              </tr>
              <tr v-for="drive in upcomingDrives" :key="'up-'+drive.id">
                <td class="ps-3 fw-bold">{{ drive.name }}</td>
                <td>
                  <span class="badge rounded-pill" :class="drive.status === 'Approved' ? 'bg-success' : 'bg-warning text-dark'">
                    {{ drive.status }}
                  </span>
                </td>
                <td><span class="badge bg-primary rounded-pill px-3">{{ drive.applicantCount || 0 }}</span></td>
                <td class="text-end pe-3">
                  <button v-if="drive.status === 'Approved'" @click="viewApplicants(drive.id)" class="btn btn-sm btn-outline-primary rounded-pill px-3 me-2">
                    Review Applicants
                  </button>
                  <button v-if="drive.status === 'Approved'" @click="closeDrive(drive.id)" class="btn btn-sm btn-outline-danger rounded-pill px-3">
                    Close Job
                  </button>
                  <button @click="deleteDrive(drive.id)" class="btn btn-sm btn-danger rounded-pill px-3 shadow-sm">
                    <i class="fa-solid fa-trash me-1"></i> Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="mb-4">
        <h5 class="text-secondary mb-3"><i class="fa-solid fa-folder-closed me-2"></i>Closed Job Postings ({{ closedDrives.length }})</h5>
        <div class="table-responsive border rounded bg-white shadow-sm">
          <table class="table table-hover mb-0 align-middle text-muted">
            <thead class="table-light">
              <tr>
                <th class="ps-3">Role</th>
                <th>Applicants</th>
                <th class="text-end pe-4">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="closedDrives.length === 0">
                <td colspan="3" class="text-center py-4">No closed jobs yet.</td>
              </tr>
              <tr v-for="drive in closedDrives" :key="'closed-'+drive.id">
                <td class="ps-3 fw-semibold">{{ drive.name }}</td>
                <td><span class="badge bg-secondary rounded-pill px-3">{{ drive.applicantCount || 0 }}</span></td>
                <td class="text-end pe-3">
                  <button @click="viewApplicants(drive.id)" class="btn btn-sm btn-outline-secondary rounded-pill px-3">
                    View History
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    
    <div v-else-if="currentView === 'postJob'" class="card shadow-sm border-0">
      <div class="card-body p-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h4 class="fw-bold mb-0">Post a New Job</h4>
          <button @click="currentView = null" class="btn btn-sm btn-outline-secondary rounded-pill px-3">Cancel</button>
        </div>
        <form @submit.prevent="submitNewJob">
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label fw-semibold text-muted small">Job Title *</label>
              <input type="text" class="form-control" v-model="jobForm.job_title" required placeholder="e.g. Software Engineer">
            </div>
            <div class="col-md-3">
              <label class="form-label fw-semibold text-muted small">Eligible Branches *</label>
              <input type="text" class="form-control" v-model="jobForm.branch" required placeholder="e.g. CSE, IT">
            </div>
            <div class="col-md-3">
              <label class="form-label fw-semibold text-muted small">Minimum CGPA</label>
              <input type="number" step="0.1" class="form-control" v-model="jobForm.min_cgpa" placeholder="0.0">
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold text-muted small">Required Skills</label>
              <input type="text" class="form-control" v-model="jobForm.required_skills" placeholder="e.g. Python, React, AWS">
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold text-muted small">Experience Required</label>
              <input type="text" class="form-control" v-model="jobForm.experience_required" placeholder="e.g. 0-2 Years, Fresher">
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold text-muted small">Salary / CTC</label>
              <input type="text" class="form-control" v-model="jobForm.salary" placeholder="e.g. 12 LPA">
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold text-muted small">Perks & Benefits</label>
              <input type="text" class="form-control" v-model="jobForm.benefits" placeholder="e.g. Health Insurance, WFH setup">
            </div>
            <div class="col-md-6">
              <label class="form-label fw-semibold text-muted small">Deadline</label>
              <input type="date" class="form-control" v-model="jobForm.deadline" required>
            </div>
            <div class="col-12">
              <label class="form-label fw-semibold text-muted small">Full Job Description *</label>
              <textarea class="form-control" v-model="jobForm.job_description" rows="5" required></textarea>
            </div>
          </div>
          <div class="mt-4 text-end">
            <button type="submit" class="btn btn-success rounded-pill px-5 fw-bold shadow-sm">Submit for Approval</button>
          </div>
        </form>
      </div>
    </div>
    
    <div v-else-if="currentView === 'applicants'" class="card shadow-sm border-0">
      <div class="card-body p-4">
        <div class="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom">
          <div>
            <h4 class="fw-bold mb-1">Applicant Pipeline</h4>
            <h6 class="text-primary mb-0">{{ activeDriveName }}</h6>
          </div>
          <button @click="currentView = null" class="btn btn-outline-primary rounded-pill px-4">
            <i class="fa-solid fa-arrow-left me-2"></i>Back to Dashboard
          </button>
        </div>
        <div v-if="applicants.length === 0" class="text-center py-5">
          <h5 class="text-muted">No students have applied for this position yet.</h5>
        </div>
        <div class="accordion" id="applicantAccordion" v-else>
          <div v-for="(app, index) in applicants" :key="'app-'+app.application_id" class="accordion-item mb-3 border rounded shadow-sm">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" :data-bs-target="'#collapse'+index">
                <div class="d-flex justify-content-between align-items-center w-100 pe-3">
                  <div>
                    <span class="fw-bold fs-5 me-3">{{ app.student_name }}</span>
                    <span class="badge bg-light text-dark border me-2">{{ app.branch }}</span>
                    <span class="badge bg-info text-dark">CGPA: {{ app.cgpa }}</span>
                  </div>
                  <span class="badge rounded-pill px-3 py-2" 
                        :class="{
                          'bg-secondary': app.status === 'Applied',
                          'bg-warning text-dark': app.status === 'Shortlisted',
                          'bg-success': app.status === 'Selected',
                          'bg-danger': app.status === 'Rejected'
                        }">
                    {{ app.status }}
                  </span>
                </div>
              </button>
            </h2>
            <div :id="'collapse'+index" class="accordion-collapse collapse" data-bs-parent="#applicantAccordion">
              <div class="accordion-body bg-light p-4">
                <div class="row mb-4">
                  <div class="col-md-8">
                    <p class="mb-1"><strong>Skills:</strong> {{ app.skills || 'Not provided' }}</p>
                    <p class="mb-1"><strong>Experience:</strong> {{ app.experience || 'Not provided' }}</p>
                    <p class="mb-1 text-muted small">Applied on: {{ app.date_applied }}</p>
                  </div>
                  <div class="col-md-4 text-end">
                    <button v-if="app.resume_path" @click="downloadResume(app.resume_path)" class="btn btn-outline-primary rounded-pill px-3">
                      <i class="fa-solid fa-file-pdf me-2"></i>View Resume
                    </button>
                  </div>
                </div>
                <hr>
                <h6 class="fw-bold text-secondary mb-3">Update Application</h6>
                <div class="row g-3 align-items-end">
                  <div class="col-md-3">
                    <label class="form-label small text-muted">Set Status</label>
                    <select class="form-select form-select-sm border-primary" v-model="app.newStatus">
                      <option value="Applied">Applied (Pending)</option>
                      <option value="Shortlisted">Shortlist for Interview</option>
                      <option value="Selected">Select (Extend Offer)</option>
                      <option value="Rejected">Reject</option>
                    </select>
                  </div>
                  <div class="col-md-3">
                    <label class="form-label small text-muted">Interview Date / Time</label>
                    <input type="date" class="form-control form-control-sm" v-model="app.newInterview">
                  </div>
                  <div class="col-md-5">
                    <label class="form-label small text-muted">Feedback to Student</label>
                    <input type="text" class="form-control form-control-sm" placeholder="Optional feedback..." v-model="app.newFeedback">
                  </div>
                  <div class="col-md-1 text-end">
                    <button @click="saveApplicantStatus(app)" class="btn btn-sm btn-success rounded-pill px-3 w-100">Save</button>
                  </div>
                </div>
                <div class="mt-4 pt-3 border-top" v-if="app.newStatus === 'Selected' || app.status === 'Selected'">
                  <h6 class="fw-bold text-success mb-3"><i class="fa-solid fa-file-contract me-2"></i>Official Offer Letter</h6>
                  <div class="d-flex align-items-center">
                    <input type="file" class="form-control form-control-sm me-3" style="max-width: 350px;" @change="handleFileUpload($event, app.application_id)" accept=".pdf">
                    <button @click="submitOfferLetter(app.application_id)" class="btn btn-sm btn-success rounded-pill px-4 shadow-sm">
                      <i class="fa-solid fa-cloud-arrow-up me-1"></i> Upload
                    </button>
                    <span v-if="app.offer_letter_path" class="badge bg-success ms-3 py-2 px-3 rounded-pill">
                      <i class="fa-solid fa-check-circle me-1"></i> Uploaded
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CompanyDashboard',
  data() {
    return {
      currentView: null,
      companyName: '',
      aboutUs: '',
      website: '',
      upcomingDrives: [],
      closedDrives: [],
      isExporting: false,
      
      // State for the Edit Profile Form
      isEditingProfile: false,
      editForm: {
        name: '',
        email: '',
        website: '',
        about_us: ''
      },

      jobForm: {
        job_title: '',
        branch: '',
        min_cgpa: '',
        required_skills: '',
        experience_required: '',
        salary: '',
        benefits: '',
        job_description: '',
        deadline: ''
      },
      activeDriveId: null,
      activeDriveName: '',
      applicants: [],
      selectedFiles: {}
    }
  },
  methods: {
    fetchDashboardData() {
      const token = localStorage.getItem('access_token');
      axios.get("http://127.0.0.1:5000/api/company/dashboard", {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        this.companyName = res.data.companyName;
        this.aboutUs = res.data.aboutUs;
        this.website = res.data.website;
        this.upcomingDrives = res.data.upcomingDrives;
        this.closedDrives = res.data.closedDrives;
      })
      .catch(err => {
        if(err.response && err.response.status === 403) {
           alert("Your account is pending admin approval. You cannot access the dashboard yet.");
           this.$router.push('/');
        }
      });
    },

    startEditing() {
      this.editForm = {
        name: this.companyName || '',
        website: this.website || '',
        about_us: this.aboutUs || ''
      };
      this.isEditingProfile = true;
    },

    saveProfile() {
      const token = localStorage.getItem('access_token');
      axios.put('http://127.0.0.1:5000/api/company/profile', this.editForm, {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        this.companyName = this.editForm.name;
        this.website = this.editForm.website;
        this.aboutUs = this.editForm.about_us;
        
        this.isEditingProfile = false;
        alert("Profile updated successfully!");
      })
      .catch(err => {
        console.error("Error updating profile:", err);
        alert("Failed to update profile. Please try again.");
      });
    },

    submitNewJob() {
      const token = localStorage.getItem('access_token');
      axios.post("http://127.0.0.1:5000/api/company/post-drive", this.jobForm, {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        alert(res.data.message);
        this.currentView = null;
        this.jobForm = { job_title: '', branch: '', min_cgpa: '', required_skills: '', experience_required: '', salary: '', benefits: '', job_description: '' };
        this.fetchDashboardData();
      })
      .catch(err => alert("Error posting job."));
    },
    viewApplicants(driveId) {
      const token = localStorage.getItem('access_token');
      axios.get(`http://127.0.0.1:5000/api/company/drive/${driveId}/applicants`, {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        this.activeDriveName = res.data.drive_name;
        this.activeDriveId = driveId;
        this.applicants = res.data.applicants.map(app => ({
          ...app,
          newStatus: app.status,
          newInterview: app.interview_date || '',
          newFeedback: app.feedback || ''
        }));
        this.currentView = 'applicants';
      })
      .catch(err => alert("Error fetching applicants."));
    },
    saveApplicantStatus(app) {
      const token = localStorage.getItem('access_token');
      axios.put(`http://127.0.0.1:5000/api/company/application/${app.application_id}/update`, 
        {
          status: app.newStatus,
          interview_date: app.newInterview,
          feedback: app.newFeedback
        },
        { headers: { "Authorization": `Bearer ${token}` } }
      )
      .then(res => {
        alert(res.data.message);
        app.status = app.newStatus;
        app.interview_date = app.newInterview;
        app.feedback = app.newFeedback;
      })
      .catch(err => alert("Error updating status."));
    },
    closeDrive(driveId) {
      if(!confirm("Are you sure you want to close this job posting? Students will no longer be able to apply.")) return;
      const token = localStorage.getItem('access_token');
      axios.post(`http://127.0.0.1:5000/api/company/drive/${driveId}/close`, {}, {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        alert("Job posting closed successfully.");
        this.fetchDashboardData();
      })
      .catch(err => alert("Error closing drive."));
    },
    deleteDrive(driveId) {
      const confirmMsg = "WARNING: Are you sure you want to completely delete this job posting?\n\nThis will permanently erase the job AND all student applications associated with it. This action CANNOT be undone.";
      
      if(!confirm(confirmMsg)) return;
      const token = localStorage.getItem('access_token');
      axios.delete(`http://127.0.0.1:5000/api/company/drive/${driveId}`, {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        alert(res.data.message);
        this.fetchDashboardData();
      })
      .catch(err => {
        console.error("Error deleting drive:", err);
        alert("There was an error permanently deleting the job posting.");
      });
    },
    downloadResume(filename) {
      const token = localStorage.getItem('access_token');
      axios.get(`http://127.0.0.1:5000/api/download-resume/${filename}`, {
        headers: { "Authorization": `Bearer ${token}` },
        responseType: 'blob' 
      })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      })
      .catch(err => alert("Error downloading resume."));
    },
    handleFileUpload(event, appId) {
      this.selectedFiles[appId] = event.target.files[0];
    },
    submitOfferLetter(appId) {
      const file = this.selectedFiles[appId];
      if (!file) {
        alert("Please select a PDF file first.");
        return;
      }
      const formData = new FormData();
      formData.append('offer_letter', file);
      const token = localStorage.getItem('access_token');
      axios.post(`http://127.0.0.1:5000/api/company/application/${appId}/upload-offer`, formData, {
        headers: { 
          "Authorization": `Bearer ${token}`,
          "Content-Type": "multipart/form-data"
        }
      })
      .then(res => {
        alert("Offer letter sent to student successfully!");
        const app = this.applicants.find(a => a.application_id === appId);
        if(app) app.offer_letter_path = res.data.path;
      })
      .catch(err => alert("Error uploading the offer letter."));
    },
    exportHistory() {
      this.isExporting = true;
      const token = localStorage.getItem('access_token');
      
      axios.post("http://127.0.0.1:5000/api/company/export-csv", {}, {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        const taskId = res.data.task_id;
        this.pollExportStatus(taskId);
      })
      .catch(err => {
        this.isExporting = false;
        alert("Error starting the export process.");
      });
    },
    pollExportStatus(taskId) {
      const token = localStorage.getItem('access_token');
      const checkStatus = () => {
        axios.get(`http://127.0.0.1:5000/api/download-export/${taskId}`, {
          headers: { "Authorization": `Bearer ${token}` },
          responseType: 'blob'
        })
        .then(res => {
          if (res.status === 202) {
            setTimeout(checkStatus, 2000);
          } else if (res.status === 200) {
            this.isExporting = false;
            
            const url = window.URL.createObjectURL(new Blob([res.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `Application_History.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          }
        })
        .catch(err => {
          this.isExporting = false;
          alert("Error downloading the export file.");
        });
      };
      
      checkStatus();
    },
  },
  mounted() {
    this.fetchDashboardData();
  }
}
</script>

<style scoped>
.accordion-button:not(.collapsed) {
  background-color: #e9ecef;
  color: #212529;
}
</style>