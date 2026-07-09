<template>
  <div class="container mt-4 mb-5" style="max-width: 900px;">
    
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-2">
      <div>
        <h4 class="mb-0 text-dark">{{ selectedApp ? 'Student Application' : 'Update Applications' }}</h4>
        <p class="text-muted mb-0 small">Job Title: {{ jobTitle }}</p>
      </div>
      
      <button v-if="selectedApp" @click="selectedApp = null" class="btn btn-sm btn-outline-secondary rounded-pill px-3">
        <i class="fa-solid fa-arrow-left me-1"></i> Back to List
      </button>
      <router-link v-else to="/company/dashboard" class="btn btn-sm btn-outline-secondary rounded-pill px-3">
        <i class="fa-solid fa-arrow-left me-1"></i> Back to Dashboard
      </router-link>
    </div>

    <div v-if="!selectedApp" class="card shadow-sm border-0">
      <div class="card-body p-4">
        <h6 class="text-secondary mb-3">Received Applications ({{ applications.length }})</h6>
        
        <div v-if="applications.length === 0" class="text-center text-muted py-4">
          No students have applied to this drive yet.
        </div>

        <ul class="list-group">
          <li v-for="app in applications" :key="app.id" class="list-group-item d-flex justify-content-between align-items-center py-3">
            <div>
              <span class="fw-semibold">{{ app.student_name }}</span>
              <span class="badge ms-2" 
                :class="{
                  'bg-secondary': app.status === 'Applied',
                  'bg-success': app.status === 'Shortlist' || app.status === 'Selected',
                  'bg-warning text-dark': app.status === 'Waiting',
                  'bg-danger': app.status === 'Reject'
                }">
                {{ app.status }}
              </span>
            </div>
            <button @click="openStudentDetails(app)" class="btn btn-sm btn-outline-primary rounded-pill px-3">
              review application
            </button>
          </li>
        </ul>
      </div>
    </div>

    <div v-else class="card shadow-sm border-0">
      <div class="card-body p-4 p-md-5">
        <div class="row">
          
          <div class="col-md-8">
            <h5 class="fw-bold mb-4 border-bottom pb-2">Application Details</h5>
            <p><strong>Student Name:</strong> {{ selectedApp.student_name }}</p>
            <p><strong>Department:</strong> {{ selectedApp.branch }}</p>
            <p><strong>Current CGPA:</strong> {{ selectedApp.cgpa }}</p>
            
            <div class="mt-4">
              <button @click="downloadResume(selectedApp.resume_path)" class="btn btn-outline-primary me-3 px-4 rounded-pill">
                <i class="fa-solid fa-file-pdf me-1"></i> view resume
              </button>
              
              <select v-model="selectedApp.status" @change="updateStatus(selectedApp)" class="form-select d-inline-block w-auto bg-light border-secondary">
                <option value="Applied" disabled>Applied</option>
                <option value="Shortlist">Shortlist</option>
                <option value="Waiting">Waiting</option>
                <option value="Reject">Reject</option>
              </select>
            </div>
          </div>

          <div class="col-md-4 d-flex justify-content-center align-items-center border-start">
            <i class="fa-solid fa-user-graduate text-secondary opacity-25" style="font-size: 8rem;"></i>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'
import { useRoute } from 'vue-router'

export default {
  name: 'DriveApplications',
  data() {
    return {
      driveId: null,
      jobTitle: 'Loading...',
      applications: [],
      selectedApp: null 
    }
  },
  methods: {
    fetchApplications() {
      const token = localStorage.getItem('access_token');
      axios.get(`http://127.0.0.1:5000/api/company/drive/${this.driveId}/applications`, {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        this.jobTitle = res.data.job_title;
        this.applications = res.data.applications;
      })
      .catch(err => console.error(err));
    },
    
    openStudentDetails(app) {
      this.selectedApp = app;
    },

    updateStatus(app) {
      const token = localStorage.getItem('access_token');
      axios.put(`http://127.0.0.1:5000/api/company/application/${app.id}/status`, 
        { status: app.status },
        { headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" } }
      )
      .then(res => {
        console.log("Status updated!");
      })
      .catch(err => alert("Error updating status."));
    },
    downloadResume(filename) {
      if (!filename) {
        alert("This student has not uploaded a resume yet.");
        return;
      }
      
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
    }
  },
  mounted() {
    const route = useRoute();
    this.driveId = this.$route.params.id;
    this.fetchApplications();
  }
}
</script>