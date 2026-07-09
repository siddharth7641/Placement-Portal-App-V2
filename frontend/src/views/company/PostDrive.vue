<template>
  <div class="container mt-4 mb-5" style="max-width: 800px;">
    
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-2">
      <h4 class="mb-0 text-dark">Post a New Drive</h4>
      <router-link to="/company/dashboard" class="btn btn-sm btn-outline-secondary rounded-pill px-3">
        <i class="fa-solid fa-arrow-left me-1"></i> Back to Dashboard
      </router-link>
    </div>

    <div class="card shadow-sm border-0">
      <div class="card-body p-4 p-md-5">
        
        <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
          <i class="fa-solid fa-circle-check me-2"></i> {{ successMessage }}
          <button type="button" class="btn-close" @click="successMessage = ''"></button>
        </div>

        <form @submit.prevent="submitDrive">
          
          <div class="row">
            <div class="col-md-12 mb-3">
              <label class="form-label fw-semibold text-secondary">Job Title <span class="text-danger">*</span></label>
              <input type="text" v-model="form.job_title" class="form-control bg-light" placeholder="e.g., Senior Vue.js Developer" required>
            </div>

            <div class="col-md-6 mb-3">
              <label class="form-label fw-semibold text-secondary">Target Branch <span class="text-danger">*</span></label>
              <select v-model="form.branch" class="form-select bg-light" required>
                <option value="" disabled>Select a branch</option>
                <option value="Computer Science">Computer Science</option>
                <option value="Data Science">Data Science</option>
                <option value="Electronics">Electronics</option>
                <option value="Mechanical">Mechanical</option>
                <option value="Any Branch">Any Branch</option>
              </select>
            </div>

            <div class="col-md-6 mb-3">
              <label class="form-label fw-semibold text-secondary">Minimum CGPA <span class="text-danger">*</span></label>
              <input type="number" step="0.1" min="0" max="10" v-model="form.min_cgpa" class="form-control bg-light" placeholder="e.g., 7.5" required>
            </div>
          </div>

          <div class="mb-4">
            <label class="form-label fw-semibold text-secondary">Job Description</label>
            <textarea v-model="form.job_description" class="form-control bg-light" rows="5" placeholder="Describe the role, responsibilities, and company perks..."></textarea>
          </div>

          <div class="d-grid mt-2">
            <button type="submit" class="btn btn-success py-2 fw-bold" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              {{ loading ? 'Posting Drive...' : 'Publish Placement Drive' }}
            </button>
          </div>

        </form>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PostDrive',
  data() {
    return {
      form: {
        job_title: '',
        branch: '',
        min_cgpa: '',
        job_description: ''
      },
      loading: false,
      successMessage: ''
    }
  },
  methods: {
    submitDrive() {
      this.loading = true;
      this.successMessage = '';
      const token = localStorage.getItem('access_token');

      axios.post("http://127.0.0.1:5000/api/company/post-drive", this.form, {
        headers: { 
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      })
      .then(res => {
        this.successMessage = res.data.message;
        this.form = { job_title: '', branch: '', min_cgpa: '', job_description: '' };
          setTimeout(() => {
          this.$router.push('/company/dashboard');
        }, 2000);
      })
      .catch(err => {
        console.error("Error posting drive:", err);
        alert("There was an error posting the drive. Please try again.");
      })
      .finally(() => {
        this.loading = false;
      });
    }
  }
}
</script>

<style scoped>
.form-control:focus, .form-select:focus {
  border-color: #198754;
  box-shadow: 0 0 0 0.25rem rgba(25, 135, 84, 0.25);
}
</style>