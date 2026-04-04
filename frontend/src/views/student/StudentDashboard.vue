<template>
  <div class="container mt-4 mb-5">
    
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
      <h4 class="mb-0 text-dark">Welcome, {{ profile.name }}</h4>
      <span class="badge bg-info rounded-pill px-3 py-2 fs-6">CGPA: {{ profile.cgpa }}</span>
    </div>

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

    <div class="d-flex justify-content-between align-items-end mb-3 mt-5">
      <h5 class="text-secondary mb-0"><i class="fa-solid fa-briefcase me-2"></i>Job Board</h5>
      <div class="d-flex">
        <input 
          type="text" 
          class="form-control form-control-sm me-2 border-primary" 
          placeholder="Search jobs or companies..." 
          v-model="searchQuery" 
          style="width: 280px;"
        >
        <button v-if="!searchQuery" class="btn btn-sm btn-outline-secondary disabled">search</button>
        <button v-else @click="searchQuery = ''" class="btn btn-sm btn-outline-danger px-3">
          <i class="fa-solid fa-xmark"></i> clear
        </button>
      </div>
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

    <h5 class="text-secondary mb-3 mt-5"><i class="fa-solid fa-list-check me-2"></i>Application Tracker</h5>
    <div v-if="appliedDrives.length === 0" class="text-center py-5 border rounded bg-light">
      <p class="text-muted mb-0">You haven't applied to any jobs yet. Check the Job Board above!</p>
    </div>
    
    <div v-else class="row">
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
</template>

<script>
import axios from 'axios'

export default {
  name: 'StudentDashboard',
  data() {
    return {
      searchQuery: '',
      isEditingProfile: false,
      selectedResume: null, // NEW: Holds the file before upload
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
    filteredAvailableDrives() {
      if (!this.searchQuery) return this.availableDrives;
      const q = this.searchQuery.toLowerCase();
      
      // FIXED: Added optional chaining (?.) so it doesn't crash if description/skills are empty!
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
    }
  },
  mounted() {
    this.fetchDashboardData();
  }
}
</script>