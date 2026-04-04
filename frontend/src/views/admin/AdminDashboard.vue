<template>
  <div class="container mt-4 mb-5">
    
    <div v-if="!selectedDrive && !selectedStudentApp" class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
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

    <div v-if="selectedDrive" class="card shadow-sm border-0 p-4">
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

    <div v-else-if="searchQuery">
      <SearchResults 
        :query="searchQuery"
        :companies="filteredRegisteredCompanies"
        :students="filteredRegisteredStudents"
        :drives="filteredOngoingDrives"
        :applications="filteredStudentApplications"
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
              {{ company.name }}
              <button class="btn btn-sm btn-outline-danger px-3 rounded-pill" @click="handleAction('company', company.id, 'blacklist')">blacklist</button>
            </li>
          </ul>
        </div>

        <div class="col-md-6 mb-4">
          <h5 class="text-secondary mb-2">Registered Students ({{ registeredStudents.length }})</h5>
          <ul class="list-group">
            <li v-for="student in registeredStudents" :key="'reg-stu-'+student.id" class="list-group-item d-flex justify-content-between align-items-center">
              {{ student.name }}
              <button class="btn btn-sm btn-outline-danger px-3 rounded-pill" @click="handleAction('student', student.id, 'blacklist')">blacklist</button>
            </li>
          </ul>
        </div>
      </div>

      <div class="mb-4">
        <h5 class="text-secondary mb-2">Company Applications ({{ filteredPendingCompanies.length }})</h5>
        <ul class="list-group border-success">
          <li v-if="filteredPendingCompanies.length === 0" class="list-group-item text-muted text-center py-3">No pending applications.</li>
          <li v-for="company in filteredPendingCompanies" :key="'pend-comp-'+company.id" class="list-group-item border-success d-flex justify-content-between align-items-center">
            {{ company.name }}
            <div>
              <button @click="handleAction('company', company.id, 'approve')" class="btn btn-sm btn-outline-success px-3 rounded-pill me-2">Approve</button>
              <button @click="handleAction('company', company.id, 'reject')" class="btn btn-sm btn-outline-danger px-3 rounded-pill">Reject</button>
            </div>
          </li>
        </ul>
      </div>

      <div class="mb-4">
        <h5 class="text-secondary mb-2">Drive Pending Applications ({{ filteredPendingDrives.length }})</h5>
        <ul class="list-group border-warning">
          <li v-if="filteredPendingDrives.length === 0" class="list-group-item text-muted text-center py-3">No pending Drives.</li>
          <li v-for="drive in filteredPendingDrives" :key="'pend-drive-'+drive.id" class="list-group-item border-warning d-flex justify-content-between align-items-center">
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
        <h5 class="text-secondary mb-2">Ongoing Drives ({{ filteredOngoingDrives.length }})</h5>
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
              <tr v-if="filteredOngoingDrives.length === 0">
                <td colspan="3" class="text-center text-muted py-3">No ongoing drives.</td>
              </tr>
              <tr v-for="(drive, index) in filteredOngoingDrives" :key="'drive-'+drive.id">
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
        <h5 class="text-secondary mb-2">Student Applications ({{ filteredStudentApplications.length }})</h5>
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
              <tr v-if="filteredStudentApplications.length === 0">
                <td colspan="6" class="text-center text-muted py-3">No applications found.</td>
              </tr>
              <tr v-for="(app, index) in filteredStudentApplications" :key="'app-'+app.id">
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
        <h5 class="text-secondary mb-2">Completed Drives ({{ filteredClosedDrives.length }})</h5>
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
              <tr v-if="filteredClosedDrives.length === 0">
                <td colspan="3" class="text-center text-muted py-3">No completed drives.</td>
              </tr>
              <tr v-for="(drive, index) in filteredClosedDrives" :key="'closed-drive-'+drive.id">
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
        <h5 class="text-secondary mb-2">Rejected Drives ({{ filteredRejectedDrives.length }})</h5>
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
              <tr v-if="filteredRejectedDrives.length === 0">
                <td colspan="3" class="text-center text-muted py-3">No rejected drives yet.</td>
              </tr>
              <tr v-for="(drive, index) in filteredRejectedDrives" :key="'rejected-drive-'+drive.id">
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
      
      registeredCompanies: [],
      blacklistedCompanies: [], 
      registeredStudents: [],
      blacklistedStudents: [], 
      pendingCompanies: [],
      ongoingDrives: [],
      studentApplications: [],
      closedDrives: [],
      pendingDrives: [],
      rejectedDrives: []
    }
  },
  
  computed: {
    filteredRegisteredCompanies() {
      if (!this.searchQuery) return this.registeredCompanies;
      const q = this.searchQuery.toLowerCase();
      return this.registeredCompanies.filter(c => 
        c.name.toLowerCase().includes(q) || 
        c.id.toString().includes(q) || 
        (c.email && c.email.toLowerCase().includes(q)) ||
        (c.phone && c.phone.toLowerCase().includes(q))
      );
    },
    filteredRegisteredStudents() {
      if (!this.searchQuery) return this.registeredStudents;
      const q = this.searchQuery.toLowerCase();
      return this.registeredStudents.filter(s => 
        s.name.toLowerCase().includes(q) || 
        s.id.toString().includes(q) || 
        (s.email && s.email.toLowerCase().includes(q)) ||
        (s.phone && s.phone.toLowerCase().includes(q))
      );
    },
    filteredPendingCompanies() {
      if (!this.searchQuery) return this.pendingCompanies;
      const q = this.searchQuery.toLowerCase();
      return this.pendingCompanies.filter(c => c.name.toLowerCase().includes(q));
    },
    filteredOngoingDrives() {
      if (!this.searchQuery) return this.ongoingDrives;
      const q = this.searchQuery.toLowerCase();
      return this.ongoingDrives.filter(d => d.name.toLowerCase().includes(q));
    },
    filteredClosedDrives() {
      if (!this.searchQuery) return this.closedDrives;
      const q = this.searchQuery.toLowerCase();
      return this.closedDrives.filter(d => d.name.toLowerCase().includes(q));
    },
    filteredStudentApplications() {
      if (!this.searchQuery) return this.studentApplications;
      const q = this.searchQuery.toLowerCase();
      return this.studentApplications.filter(app => 
        app.studentName.toLowerCase().includes(q) ||
        app.companyName.toLowerCase().includes(q) ||
        app.driveName.toLowerCase().includes(q)
      );
    },
    filteredPendingDrives() {
      if (!this.searchQuery) return this.pendingDrives;
      const q = this.searchQuery.toLowerCase();
      return this.pendingDrives.filter(d => 
        d.name.toLowerCase().includes(q) || 
        (d.company && d.company.toLowerCase().includes(q))
      );
    },
    filteredRejectedDrives() {
      if (!this.searchQuery) return this.rejectedDrives;
      const q = this.searchQuery.toLowerCase();
      return this.rejectedDrives.filter(d => 
        d.name.toLowerCase().includes(q) || 
        (d.company && d.company.toLowerCase().includes(q))
      );
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