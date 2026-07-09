<template>
  <div class="container mt-4 mb-5">
    
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
      <h4 class="mb-0 text-dark">Welcome, {{ profile.name }}</h4>
      <span class="badge bg-info rounded-pill px-3 py-2 fs-6">CGPA: {{ profile.cgpa }}</span>
    </div>

    <div v-if="selectedCompany" class="card shadow-sm border-0 p-4 mb-5">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h4 class="fw-bold mb-1"><i class="fa-regular fa-building me-2 text-primary"></i>{{ selectedCompany.name }}</h4>
          <a v-if="selectedCompany.website" :href="selectedCompany.website" target="_blank" class="text-primary small text-decoration-none">
            <i class="fa-solid fa-link me-1"></i>{{ selectedCompany.website }}
          </a>
        </div>
        <button @click="selectedCompany = null" class="btn btn-outline-secondary rounded-pill px-4">
          <i class="fa-solid fa-arrow-left me-2"></i>Back to Dashboard
        </button>
      </div>

      <div class="mb-4 p-4 bg-light rounded border">
        <h6 class="fw-bold text-secondary mb-2">About the Company</h6>
        <p class="mb-0 text-dark" style="white-space: pre-line;">{{ selectedCompany.overview }}</p>
      </div>

      <h5 class="text-secondary mb-3 mt-4"><i class="fa-solid fa-briefcase me-2"></i>Active Roles at {{ selectedCompany.name }}</h5>
      <div class="list-group shadow-sm">
         <div v-if="selectedCompany.drives.length === 0" class="list-group-item text-muted text-center py-4 bg-light">
           No active job postings from this company at the moment.
         </div>
         <div v-for="drive in selectedCompany.drives" :key="'comp-drive-'+drive.id" class="list-group-item d-flex justify-content-between align-items-center p-3">
             <div class="me-4">
                <h6 class="fw-bold mb-1">{{ drive.job_title }}</h6>
                
                <p class="mb-0 small text-muted">{{ (drive.job_description || 'No description provided.').substring(0, 100) }}...</p>
             </div>
             <div>
               <button
                  @click="applyForJob(drive.id)"
                  class="btn btn-sm btn-primary rounded-pill px-4 text-nowrap"
                  :disabled="drive.has_applied "
                  :title="!profile.resume_path ? 'Upload resume first' : ''"
               >
                  {{ drive.has_applied ? 'Applied' : 'Apply Now' }}
               </button>
             </div>
         </div>
      </div>
    </div>

    <div v-else>
      <div class="card shadow-sm border-0 mb-5">
        <div class="card-body p-4">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="text-secondary mb-0"><i class="fa-solid fa-user-graduate me-2"></i>My Profile</h5>
            <button @click="openEditProfile" class="btn btn-sm btn-outline-primary rounded-pill px-3">
              <i class="fa-solid fa-pen-to-square me-1"></i> Edit
            </button>
          </div>
          
          <div class="row" v-if="!isEditingProfile">
            <div class="col-md-6">
              <p><strong>Email:</strong> {{ profile.email || 'Not provided' }}</p>
              <p><strong>Phone:</strong> {{ profile.phone || 'Not provided' }}</p>
              <p><strong>Branch:</strong> {{ profile.branch || 'Not provided' }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Skills:</strong> {{ profile.skills || 'Add your skills!' }}</p>
              <p><strong>Experience:</strong> {{ profile.experience || 'Add your experience!' }}</p>
              
              <p class="mb-2">
                <strong>Resume:</strong> 
                <span v-if="profile.resume_path" class="text-success fw-bold"><i class="fa-solid fa-check-circle me-1"></i>Uploaded</span>
                <span v-else class="text-danger fw-bold"><i class="fa-solid fa-times-circle me-1"></i>Not uploaded</span>
              </p>
              <div class="d-flex align-items-center">
                <input type="file" class="form-control form-control-sm me-2" style="max-width: 250px;" @change="handleResumeUpload" accept=".pdf">
                <button @click="submitResume" class="btn btn-sm btn-success rounded-pill px-3 shadow-sm" :disabled="!selectedResume">
                  <i class="fa-solid fa-upload me-1"></i> Upload
                </button>
              </div>
            </div>
          </div>

          <div v-if="isEditingProfile" class="mt-3 p-3 bg-light rounded border">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label text-muted small">Full Name</label>
                <input type="text" class="form-control form-control-sm" v-model="editForm.name">
              </div>
              <div class="col-md-6">
                <label class="form-label text-muted small">Email</label>
                <input type="email" class="form-control form-control-sm" v-model="editForm.email">
              </div>
              <div class="col-md-4">
                <label class="form-label text-muted small">Phone</label>
                <input type="text" class="form-control form-control-sm" v-model="editForm.phone">
              </div>
              <div class="col-md-4">
                <label class="form-label text-muted small">Branch</label>
                <input type="text" class="form-control form-control-sm" v-model="editForm.branch">
              </div>
              <div class="col-md-4">
                <label class="form-label text-muted small">CGPA</label>
                <input type="number" step="0.1" class="form-control form-control-sm" v-model="editForm.cgpa">
              </div>
              <div class="col-12">
                <label class="form-label text-muted small">Skills (e.g., Python, Vue.js, SQL)</label>
                <input type="text" class="form-control form-control-sm" v-model="editForm.skills">
              </div>
              <div class="col-12">
                <label class="form-label text-muted small">Experience / Projects</label>
                <textarea class="form-control form-control-sm" v-model="editForm.experience" rows="2"></textarea>
              </div>
            </div>
            <div class="mt-3 d-flex justify-content-end">
              <button @click="isEditingProfile = false" class="btn btn-sm btn-outline-secondary me-2 px-3 rounded-pill">Cancel</button>
              <button @click="saveProfile" class="btn btn-sm btn-success px-4 rounded-pill">Save Changes</button>
            </div>
          </div>
        </div>
      </div>
      <div class="d-flex w-100">
          <input 
            type="text" 
            class="form-control form-control-sm me-2 border-primary w-100" 
            placeholder="Search jobs or companies..." 
            v-model="searchQuery" 
            style="max-width: 500px;" 
          >
          <button v-if="!searchQuery" class="btn btn-sm btn-outline-secondary disabled">Search</button>
          <button v-else @click="searchQuery = ''" class="btn btn-sm btn-outline-danger px-3">
            <i class="fa-solid fa-xmark"></i> Clear
          </button>
        </div>
        
      <h5 class="text-secondary mb-3 mt-5"><i class="fa-regular fa-building me-2"></i>Participating Organizations</h5>
      <div class="row mb-5">
        
        <div v-if="filteredOrganizations.length === 0" class="col-12 text-center py-4 bg-light rounded border text-muted">
          No companies match your search.
        </div>
        
        <div class="col-md-4 mb-3" v-for="org in filteredOrganizations" :key="'org-'+org.id">
          <div class="card shadow-sm border-0 h-100 border-start border-4 border-primary">
            <div class="card-body d-flex flex-column justify-content-center">
              <div class="d-flex justify-content-between align-items-center">
                <span class="fw-bold text-dark fs-5">{{ org.name }}</span>
                <button @click="viewCompany(org.id)" class="btn btn-sm btn-outline-primary rounded-pill px-3">View Details</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="d-flex justify-content-between align-items-end mb-3 mt-5">
        <h5 class="text-secondary mb-0"><i class="fa-solid fa-briefcase me-2"></i>Job Board</h5>
      </div>

      <div class="card shadow-sm border-0 mb-5">
        <div class="table-responsive border rounded bg-white">
          <table class="table table-hover mb-0 align-middle">
            <thead class="table-light">
              <tr>
                <th class="ps-3">Company</th>
                <th>Role</th>
                <th>Branch Reqs</th>
                <th>Min CGPA</th>
                <th class="text-end pe-4">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredAvailableDrives.length === 0">
                <td colspan="5" class="text-center text-muted py-4">No job postings match your search.</td>
              </tr>
              <tr v-for="drive in filteredAvailableDrives" :key="'avail-'+drive.id">
                <td class="ps-3 fw-semibold">{{ drive.company_name }}</td>
                <td>{{ drive.job_title }}</td>
                <td><span class="badge bg-light text-dark border">{{ drive.branch }}</span></td>
                <td>
                  <span :class="{'text-danger fw-bold': profile.cgpa < drive.min_cgpa}">
                    {{ drive.min_cgpa }}
                  </span>
                </td>
                <td class="text-end pe-3">
                  <button 
                    @click="applyForJob(drive.id)" 
                    class="btn btn-sm btn-primary rounded-pill px-4"
                    :disabled="profile.cgpa < drive.min_cgpa || hasApplied(drive.id) || !profile.resume_path"
                    :title="!profile.resume_path ? 'You must upload a resume first!' : ''"
                  >
                    {{ hasApplied(drive.id) ? 'Applied' : 'Apply' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="d-flex justify-content-between align-items-center mb-3 mt-5 border-bottom pb-2">
        <h5 class="text-secondary mb-0"><i class="fa-solid fa-list-check me-2"></i>Application Tracker</h5>
        
        <button 
          @click="exportHistory" 
          class="btn btn-sm btn-outline-success rounded-pill px-4 shadow-sm"
          :disabled="isExporting || appliedDrives.length === 0"
          >
          <span v-if="isExporting"><i class="fa-solid fa-spinner fa-spin me-2"></i> Generating CSV...</span>
          <span v-else><i class="fa-solid fa-file-csv me-1"></i> Export History</span>
        </button>
      </div>

      <div v-if="appliedDrives.length === 0" class="text-center py-5 border rounded bg-light mb-5">
        <p class="text-muted mb-0">You haven't applied to any jobs yet. Check the Job Board above!</p>
      </div>
      
      <div v-else class="row mb-5">
        <div v-for="app in appliedDrives" :key="'app-'+app.id" class="col-12 mb-3">
          <div class="card shadow-sm border-0">
            <div class="card-body p-4 d-flex justify-content-between align-items-center">
              <div>
                <h5 class="mb-1 fw-bold">{{ app.drive_name }}</h5>
                <h6 class="text-muted mb-2">{{ app.company_name }} <span class="mx-2">|</span> Applied: {{ app.date }}</h6>
                
                <div v-if="app.interview_date || app.feedback" class="mt-3 p-3 bg-light rounded border border-warning">
                  <p v-if="app.interview_date" class="mb-1 text-dark small">
                    <i class="fa-regular fa-calendar-check text-warning me-2"></i><strong>Interview Scheduled:</strong> {{ app.interview_date }}
                  </p>
                  <p v-if="app.feedback" class="mb-0 text-dark small">
                    <i class="fa-regular fa-comment-dots text-secondary me-2"></i><strong>Feedback:</strong> "{{ app.feedback }}"
                  </p>
                </div>
              </div>

              <div class="text-end">
                <span class="badge rounded-pill px-4 py-2 fs-6 mb-3 d-inline-block" 
                      :class="{
                        'bg-secondary': app.status === 'Applied',
                        'bg-warning text-dark': app.status === 'Shortlisted',
                        'bg-success': app.status === 'Selected',
                        'bg-danger': app.status === 'Rejected'
                      }">
                  {{ app.status }}
                </span>
                <br>
                <button v-if="app.status === 'Selected' && app.offer_letter_path" 
                        @click="downloadOfferLetter(app.offer_letter_path)" 
                        class="btn btn-sm btn-outline-success rounded-pill px-3 mt-2">
                  <i class="fa-solid fa-file-contract me-1"></i> Download Offer
                </button>
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
  name: 'StudentDashboard',
  data() {
    return {
      searchQuery: '',
      isEditingProfile: false,
      isExporting: false,
      selectedResume: null, 
      selectedCompany: null, 
      organizations: [],     
      profile: {
        name: '',
        email: '',
        phone: '',
        branch: '',
        cgpa: 0,
        resume_path: null,
        skills: '',
        experience: ''
      },
      editForm: { ...this.profile },
      availableDrives: [],
      appliedDrives: []
    }
  },
  
  computed: {
    filteredOrganizations() {
      if (!this.searchQuery) {
        return this.organizations;
      }
      const query = this.searchQuery.toLowerCase();
      
      return this.organizations.filter(org => {
        return org.name.toLowerCase().includes(query);
      });
    },
    filteredAvailableDrives() {
      if (!this.searchQuery) return this.availableDrives;
      const q = this.searchQuery.toLowerCase();
      
      return this.availableDrives.filter(drive => 
        drive.job_title?.toLowerCase().includes(q) || 
        drive.company_name?.toLowerCase().includes(q) ||
        drive.branch?.toLowerCase().includes(q) ||
        drive.description?.toLowerCase().includes(q) ||
        drive.skills?.toLowerCase().includes(q)
      );
    }
  },

  methods: {
    fetchDashboardData() {
      const token = localStorage.getItem('access_token');
      axios.get("http://127.0.0.1:5000/api/student/dashboard", {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        this.profile.name = res.data.studentName;
        this.profile.email = res.data.email;
        this.profile.phone = res.data.phone;
        this.profile.branch = res.data.branch;
        this.profile.cgpa = res.data.cgpa;
        this.profile.resume_path = res.data.resume_path;
        this.profile.skills = res.data.skills;
        this.profile.experience = res.data.experience;
        
        this.organizations = res.data.organizations; 
        this.availableDrives = res.data.availableDrives;
        this.appliedDrives = res.data.appliedDrives;
      })
      .catch(err => console.error("Error fetching dashboard:", err));
    },

    openEditProfile() {
      this.editForm = { ...this.profile };
      this.isEditingProfile = true;
    },

    saveProfile() {
      const token = localStorage.getItem('access_token');
      axios.put("http://127.0.0.1:5000/api/student/profile", 
        {
          full_name: this.editForm.name,
          email: this.editForm.email,
          phone: this.editForm.phone,
          branch: this.editForm.branch,
          cgpa: this.editForm.cgpa,
          skills: this.editForm.skills,
          experience: this.editForm.experience
        },
        { headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" } }
      )
      .then(res => {
        this.isEditingProfile = false;
        this.fetchDashboardData();
        alert("Profile updated successfully!");
      })
      .catch(err => alert("Error updating profile."));
    },

    handleResumeUpload(event) {
      this.selectedResume = event.target.files[0];
    },

    submitResume() {
      if (!this.selectedResume) return;
      
      const formData = new FormData();
      formData.append('resume', this.selectedResume);
      
      const token = localStorage.getItem('access_token');
      axios.post('http://127.0.0.1:5000/api/student/upload-resume', formData, {
        headers: { 
          'Authorization': `Bearer ${token}`, 
          'Content-Type': 'multipart/form-data' 
        }
      })
      .then(res => {
        alert("Resume uploaded successfully!");
        this.fetchDashboardData(); 
        this.selectedResume = null; 
      })
      .catch(err => alert("Error uploading resume. Make sure it is a PDF."));
    },

    viewCompany(companyId) {
      const token = localStorage.getItem('access_token');
      axios.get(`http://127.0.0.1:5000/api/student/company/${companyId}`, {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        this.selectedCompany = res.data;
      })
      .catch(err => alert("Error fetching company details."));
    },

    hasApplied(driveId) {
      return this.appliedDrives.some(app => app.drive_id === driveId);
    },

    applyForJob(driveId) {
      if(!confirm("Are you sure you want to apply for this position?")) return;
      
      const token = localStorage.getItem('access_token');
      axios.post(`http://127.0.0.1:5000/api/student/apply/${driveId}`, {}, {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        alert("Successfully applied!");
        this.fetchDashboardData(); 
        if(this.selectedCompany) this.viewCompany(this.selectedCompany.id);
      })
      .catch(err => {
        alert(err.response?.data?.message || "Error applying for job.");
      });
    },

    downloadOfferLetter(filename) {
      const token = localStorage.getItem('access_token');
      axios.get(`http://127.0.0.1:5000/api/download-offer/${filename}`, {
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
      .catch(err => alert("Error downloading offer letter."));
    },
    exportHistory() {
      this.isExporting = true;
      const token = localStorage.getItem('access_token');
      
      axios.post("http://127.0.0.1:5000/api/student/export-csv", {}, {
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