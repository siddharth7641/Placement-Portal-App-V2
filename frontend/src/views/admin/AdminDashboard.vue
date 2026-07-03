<template>
  <div class="container mt-4 mb-5">
    
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
         </div>
      </div>
    </div>

    <div v-else-if="selectedStudent" class="card shadow-sm border-0 p-4 mb-5">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h4 class="fw-bold mb-1"><i class="fa-solid fa-user-graduate me-2 text-primary"></i>{{ selectedStudent.name }}</h4>
          <p class="text-muted mb-0 mt-2">
            <span class="me-3"><i class="fa-solid fa-envelope me-2"></i>{{ selectedStudent.email || 'No email provided' }}</span>
            <span><i class="fa-solid fa-phone me-2"></i>{{ selectedStudent.phone || 'No phone provided' }}</span>
          </p>
        </div>
        <button @click="selectedStudent = null" class="btn btn-outline-secondary rounded-pill px-4">
          <i class="fa-solid fa-arrow-left me-2"></i>Back to Dashboard
        </button>
      </div>

      <h5 class="text-secondary mb-3 mt-4"><i class="fa-solid fa-file-lines me-2"></i>Application History</h5>
      <div class="list-group shadow-sm">
         <div v-if="selectedStudent.applications.length === 0" class="list-group-item text-muted text-center py-4 bg-light">
           This student has not applied to any placement drives yet.
         </div>

         <div v-for="app in selectedStudent.applications" :key="'stu-app-'+app.id" class="list-group-item d-flex justify-content-between align-items-center p-3">
             <div>
                <h6 class="fw-bold mb-1">Drive ID: {{ app.drive_id }}</h6>
             </div>
             <div>
               <span class="badge px-3 py-2 rounded-pill bg-primary">
                 {{ app.status }}
               </span>
             </div>
         </div>
      </div>
    </div>

    <div v-else-if="selectedDrive" class="card shadow-sm border-0 p-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h4 class="fw-bold mb-0">Drive Details</h4>
        <span class="badge px-3 py-2 fs-6 rounded-pill" 
              :class="{
                'bg-warning text-dark': selectedDrive.status === 'Pending',
                'bg-success': selectedDrive.status === 'Approved',
                'bg-secondary': selectedDrive.status === 'Closed',
                'bg-danger': selectedDrive.status === 'Rejected'
              }">
          {{ selectedDrive.status }}
        </span>
      </div>

      <div class="row">
        <div class="col-md-8">
          <h5 class="text-primary fw-bold mb-3">{{ selectedDrive.name }}</h5>
          <div class="row mb-3">
            <div class="col-sm-6">
              <p class="mb-1"><i class="fa-regular fa-building me-2 text-muted"></i><strong>Company:</strong> {{ selectedDrive.company }}</p>
              <p class="mb-1"><i class="fa-solid fa-graduation-cap me-2 text-muted"></i><strong>Min CGPA:</strong> {{ selectedDrive.min_cgpa }}</p>
            </div>
            <div class="col-sm-6">
              <p class="mb-1"><i class="fa-solid fa-code-branch me-2 text-muted"></i><strong>Branches:</strong> {{ selectedDrive.branch }}</p>
            </div>
          </div>

          <div class="mt-4 p-4 bg-light rounded border">
            <h6 class="fw-bold text-secondary mb-2"><i class="fa-solid fa-align-left me-2"></i>Job Description</h6>
            <p class="mb-0 text-dark" style="white-space: pre-line;">
              {{ selectedDrive.description || 'No description provided.' }}
            </p>
          </div>

          <div class="mt-5">
            <button @click="selectedDrive = null" class="btn btn-outline-primary px-4 rounded-pill">
              <i class="fa-solid fa-arrow-left me-2"></i> Go Back
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="selectedStudentApp" class="card shadow-sm border-0 p-4">
      <h4 class="mb-4 fw-bold">Student Application</h4>
      <div class="row">
        <div class="col-md-8">
          <p><strong>Student Name:</strong> {{ selectedStudentApp.studentName }}</p>
          <p><strong>Drive:</strong> {{ selectedStudentApp.driveName }}</p>
          <div class="mt-5">
            <button @click="downloadResume(selectedStudentApp.resume_path)" class="btn btn-outline-primary px-4 rounded-pill me-3">
              <i class="fa-solid fa-file-pdf me-1"></i> view resume
            </button>
            <button @click="selectedStudentApp = null" class="btn btn-outline-secondary px-4 rounded-pill">back</button>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
        <h4 class="mb-0 text-dark">Welcome Admin</h4>
        <div class="d-flex">
          <input 
            type="text" 
            class="form-control form-control-sm me-2" 
            placeholder="Search names, companies, drives..." 
            v-model="searchQuery" 
            style="width: 300px;"
          >
          <button v-if="!searchQuery" class="btn btn-sm btn-outline-secondary disabled">search</button>
          <button v-else @click="searchQuery = ''" class="btn btn-sm btn-outline-danger px-3">
            <i class="fa-solid fa-xmark"></i> clear
          </button>
        </div>
      </div>

      <div v-if="searchQuery">
        <SearchResults 
          :query="searchQuery"
          :companies="searchResults.companies"
          :students="searchResults.students"
          :drives="searchResults.drives"
          :applications="searchResults.applications"
          
          @blacklist-company="(id) => handleAction('company', id, 'blacklist')"
          @blacklist-student="(id) => handleAction('student', id, 'blacklist')"
          @view-drive="(drive) => selectedDrive = drive"
          @view-application="(app) => selectedStudentApp = app"
        />
      </div>

      <div v-else>
        <div class="row">
          <div class="col-md-6 mb-4">
            <h5 class="text-secondary mb-2">Registered Companies ({{ registeredCompanies.length }})</h5>
            <ul class="list-group">
              <li v-for="company in registeredCompanies" :key="'reg-comp-'+company.id" class="list-group-item d-flex justify-content-between align-items-center">
                
                <div>
                  <span class="text-muted small me-2">#{{ company.id }}</span>
                  <span class="fw-medium">{{ company.name }}</span>
                </div>
                
                <div class="d-flex gap-2">
                  <button class="btn btn-sm btn-outline-primary px-3 rounded-pill" @click="viewCompanyDetails(company.id)">View Details</button>
                  <button class="btn btn-sm btn-outline-danger px-3 rounded-pill" @click="handleAction('company', company.id, 'blacklist')">Blacklist</button>
                </div>
              </li>
            </ul>
          </div>

          <div class="col-md-6 mb-4">
            <h5 class="text-secondary mb-2">Registered Students ({{ registeredStudents.length }})</h5>
            <ul class="list-group">
              <li v-for="student in registeredStudents" :key="'reg-stu-'+student.id" class="list-group-item d-flex justify-content-between align-items-center">
                
                <div>
                  <span class="text-muted small me-2">#{{ student.id }}</span>
                  <span class="fw-medium">{{ student.name }}</span>
                </div>
                
                <div class="d-flex gap-2">
                  <button class="btn btn-sm btn-outline-primary px-3 rounded-pill" @click="viewStudentDetails(student.id)">View Details</button>
                  <button class="btn btn-sm btn-outline-danger px-3 rounded-pill" @click="handleAction('student', student.id, 'blacklist')">Blacklist</button>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <div class="mb-4">
          <h5 class="text-secondary mb-2">Company Applications ({{ pendingCompanies.length }})</h5>
          <ul class="list-group border-success">
            <li v-if="pendingCompanies.length === 0" class="list-group-item text-muted text-center py-3">No pending applications.</li>
            <li v-for="company in pendingCompanies" :key="'pend-comp-'+company.id" class="list-group-item border-success d-flex justify-content-between align-items-center">
              {{ company.name }}
              <div>
                <button @click="handleAction('company', company.id, 'approve')" class="btn btn-sm btn-outline-success px-3 rounded-pill me-2">Approve</button>
                <button @click="handleAction('company', company.id, 'reject')" class="btn btn-sm btn-outline-danger px-3 rounded-pill">Reject</button>
              </div>
            </li>
          </ul>
        </div>

        <div class="mb-4">
          <h5 class="text-secondary mb-2">Drive Pending Applications ({{ pendingDrives.length }})</h5>
          <ul class="list-group border-warning">
            <li v-if="pendingDrives.length === 0" class="list-group-item text-muted text-center py-3">No pending Drives.</li>
            <li v-for="drive in pendingDrives" :key="'pend-drive-'+drive.id" class="list-group-item border-warning d-flex justify-content-between align-items-center">
              <div>
                <span class="fw-bold text-dark">{{ drive.name }}</span> 
                <span class="text-muted small ms-2">by {{ drive.company }}</span>
              </div>
              <div>
                <button @click="handleAction('drive', drive.id, 'approve')" class="btn btn-sm btn-outline-success px-3 rounded-pill me-2">Approve</button>
                <button @click="handleAction('drive', drive.id, 'reject')" class="btn btn-sm btn-outline-danger px-3 rounded-pill">Reject</button>
              </div>
            </li>
          </ul>
        </div>

        <div class="mb-4">
          <h5 class="text-secondary mb-2">Ongoing Drives ({{ ongoingDrives.length }})</h5>
          <div class="table-responsive border rounded bg-white">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>Sr No.</th>
                  <th>Drive Name</th>
                  <th class="text-end pe-4">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="ongoingDrives.length === 0">
                  <td colspan="3" class="text-center text-muted py-3">No ongoing drives.</td>
                </tr>
                <tr v-for="(drive, index) in ongoingDrives" :key="'drive-'+drive.id">
                  <td>{{ index + 1 }}.</td>
                  <td>{{ drive.name }}</td>
                  <td class="text-end">
                    <button @click="selectedDrive = drive" class="btn btn-sm btn-outline-primary me-2 rounded-pill">view details</button>
                    <button class="btn btn-sm btn-outline-success rounded-pill" @click="markAsComplete(drive.id)">mark as complete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="mb-5">
          <h5 class="text-secondary mb-2">Student Applications ({{ studentApplications.length }})</h5>
          <div class="table-responsive border rounded bg-white">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>Sr No.</th>
                  <th>Name</th>
                  <th>Drive</th>
                  <th>Company</th>
                  <th>Date</th>
                  <th class="text-end pe-4">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="studentApplications.length === 0">
                  <td colspan="6" class="text-center text-muted py-3">No applications found.</td>
                </tr>
                <tr v-for="(app, index) in studentApplications" :key="'app-'+app.id">
                  <td>{{ index + 1 }}.</td>
                  <td>{{ app.studentName }}</td>
                  <td>{{ app.driveName }}</td>
                  <td>{{ app.companyName }}</td>
                  <td>{{ app.date }}</td>
                  <td class="text-end">
                    <button @click="selectedStudentApp = app" class="btn btn-sm btn-outline-primary rounded-pill px-3">view</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="mb-4">
          <h5 class="text-secondary mb-2">Completed Drives ({{ closedDrives.length }})</h5>
          <div class="table-responsive border rounded bg-white">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>Sr No.</th>
                  <th>Drive Name</th>
                  <th class="text-end pe-4">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="closedDrives.length === 0">
                  <td colspan="3" class="text-center text-muted py-3">No completed drives.</td>
                </tr>
                <tr v-for="(drive, index) in closedDrives" :key="'closed-drive-'+drive.id">
                  <td>{{ index + 1 }}.</td>
                  <td class="text-muted">{{ drive.name }}</td>
                  <td class="text-end">
                    <button @click="selectedDrive = drive" class="btn btn-sm btn-outline-secondary rounded-pill px-3">
                      view details
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="mb-4">
          <h5 class="text-secondary mb-2">Rejected Drives ({{ rejectedDrives.length }})</h5>
          <div class="table-responsive border rounded bg-white">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>Sr No.</th>
                  <th>Drive Name</th>
                  <th class="text-end pe-4">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="rejectedDrives.length === 0">
                  <td colspan="3" class="text-center text-muted py-3">No rejected drives yet.</td>
                </tr>
                <tr v-for="(drive, index) in rejectedDrives" :key="'rejected-drive-'+drive.id">
                  <td>{{ index + 1 }}.</td>
                  <td class="text-muted">{{ drive.name }}</td>
                  <td class="text-end">
                    <button @click="selectedDrive = drive" class="btn btn-sm btn-outline-secondary rounded-pill px-3">
                      view details
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-if="blacklistedCompanies.length > 0 || blacklistedStudents.length > 0" class="mb-5 p-4 bg-white border border-danger rounded shadow-sm">
          <h5 class="text-danger fw-bold mb-3"><i class="fa-solid fa-ban me-2"></i> Restricted Accounts</h5>
          <div class="row">
            <div class="col-md-6" v-if="blacklistedCompanies.length > 0">
              <h6 class="text-muted">Suspended Companies</h6>
              <ul class="list-group">
                <li v-for="company in blacklistedCompanies" :key="'banned-comp-'+company.id" class="list-group-item list-group-item-danger d-flex justify-content-between align-items-center">
                  {{ company.name }}
                  <button class="btn btn-sm btn-success px-3 rounded-pill" @click="handleAction('company', company.id, 'unblacklist')">Unblacklist</button>
                </li>
              </ul>
            </div>
            <div class="col-md-6" v-if="blacklistedStudents.length > 0">
              <h6 class="text-muted">Suspended Students</h6>
              <ul class="list-group">
                <li v-for="student in blacklistedStudents" :key="'banned-stu-'+student.id" class="list-group-item list-group-item-danger d-flex justify-content-between align-items-center">
                  {{ student.name }}
                  <button class="btn btn-sm btn-success px-3 rounded-pill" @click="handleAction('student', student.id, 'unblacklist')">Unblacklist</button>
                </li>
              </ul>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SearchResults from '../../components/SearchResults.vue'

export default {
  name: 'AdminDashboard',
  components: {
    SearchResults
  },
  data() {
    return {
      searchQuery: '',
      selectedDrive: null,
      selectedStudentApp: null,
      selectedCompany: null,
      selectedStudent: null,

      registeredCompanies: [],
      blacklistedCompanies: [], 
      registeredStudents: [],
      blacklistedStudents: [], 
      pendingCompanies: [],
      ongoingDrives: [],
      studentApplications: [],
      closedDrives: [],
      pendingDrives: [],
      rejectedDrives: [],

      searchTimeout: null, 
      searchResults: {
        companies: [],
        students: [],
        drives: [],
        applications: []
      },
    }
  },
  methods: {
    fetchDashboardData() {
      const token = localStorage.getItem('access_token');
      const config = { headers: { "Authorization": `Bearer ${token}` } };

      axios.get("http://127.0.0.1:5000/api/admin/dashboard", config)
      .then(res => {
        this.registeredCompanies = res.data.registeredCompanies;
        this.blacklistedCompanies = res.data.blacklistedCompanies;
        this.registeredStudents = res.data.registeredStudents;
        this.blacklistedStudents = res.data.blacklistedStudents;
        this.ongoingDrives = res.data.ongoingDrives;
        this.closedDrives = res.data.closedDrives;
        this.studentApplications = res.data.studentApplications;
        this.pendingDrives = res.data.pendingDrives;
        this.rejectedDrives = res.data.rejectedDrives;
      }).catch(err => console.error(err));

      axios.get("http://127.0.0.1:5000/api/admin/pending-companies", config)
      .then(res => this.pendingCompanies = res.data)
      .catch(err => {
        console.error("Error fetching company stats:", err);
        if (err.response && err.response.status === 401) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('user_role');
          this.$router.push('/admin');
        }
      });
    },
    performBackendSearch(query) {
      const token = localStorage.getItem('access_token');
      axios.get(`http://127.0.0.1:5000/api/admin/search?q=${query}`, {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        this.searchResults = res.data;
      })
      .catch(err => console.error("Search failed:", err));
    },
    viewCompanyDetails(companyId) {
      const token = localStorage.getItem('access_token');
      axios.get(`http://127.0.0.1:5000/api/company_details/${companyId}`, {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        this.selectedCompany = res.data;
      })
      .catch(err => alert("Error fetching company details."));
    },
    viewStudentDetails(studentId) {
      const token = localStorage.getItem('access_token');
      axios.get(`http://127.0.0.1:5000/api/student_details/${studentId}`, {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        this.selectedStudent = res.data;
      })
      .catch(err => {
        console.error(err);
        alert("Error fetching student details from the server.");
      });
    },
    handleAction(type, id, action) {
      if(action === 'blacklist' && !confirm(`Are you sure you want to suspend this ${type}?`)) return;
      if(action === 'reject' && !confirm(`Are you sure you want to reject this ${type} application?`)) return;
      
      const token = localStorage.getItem('access_token');
      let endpoint = '';
      if (type === 'company') endpoint = `/api/admin/company-action/${id}`;
      else if (type === 'student') endpoint = `/api/admin/student-action/${id}`;
      else if (type === 'drive') endpoint = `/api/admin/drive-action/${id}`;
      
      axios.post(`http://127.0.0.1:5000${endpoint}`, 
        { action: action }, 
        { headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" } }
      )
      .then(() => this.fetchDashboardData())
      .catch(() => alert(`Error processing ${action}.`));
    },

    markAsComplete(driveId) {
      if(!confirm("Are you sure you want to mark this drive as complete? Students will no longer be able to apply.")) {
        return;
      }
      const token = localStorage.getItem('access_token');
      axios.post(`http://127.0.0.1:5000/api/admin/drive/${driveId}/close`, {}, {
        headers: { "Authorization": `Bearer ${token}` }
      })
      .then(res => {
        this.fetchDashboardData();
      })
      .catch(err => {
        console.error("Error closing drive:", err);
        alert("There was an error closing the drive.");
      });
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
  watch: {
    searchQuery(newVal) {
      clearTimeout(this.searchTimeout);
      if (!newVal.trim()) {
        this.searchResults = { companies: [], students: [], drives: [], applications: [] };
        return;
      }
      this.searchTimeout = setTimeout(() => {
        this.performBackendSearch(newVal);
      }, 300);
    }
  },
  mounted() {
    this.fetchDashboardData();
  }
}
</script>

<style scoped>
.list-group-item { border-radius: 0; margin-bottom: 5px; border: 1px solid #dee2e6; }
.list-group-item.border-success { border-color: #28a745 !important; }
.text-secondary { color: #555 !important; font-weight: 500; }
</style>
