<template>
  <div class="container mt-5 mb-5">
    <div class="row justify-content-center">
      <div class="col-md-7">
        <div class="card shadow-lg border-0 p-5">
          <div class="text-center mb-4">
            <h3 class="fw-bold">Create an Account</h3>
            <p class="text-muted">Join the placement portal today.</p>
          </div>

          <form @submit.prevent="registerUser">
            
            <div class="mb-4 text-center">
              <label class="form-label fw-bold d-block mb-3">I am a:</label>
              <div class="btn-group w-100" role="group">
                <input type="radio" class="btn-check" name="role" id="roleStudent" value="student" v-model="formData.role">
                <label class="btn btn-outline-primary py-2" for="roleStudent"><i class="fa-solid fa-user-graduate me-2"></i>Student</label>

                <input type="radio" class="btn-check" name="role" id="roleCompany" value="company" v-model="formData.role">
                <label class="btn btn-outline-primary py-2" for="roleCompany"><i class="fa-solid fa-building me-2"></i>Company</label>
              </div>
            </div>

            <div class="form-floating mb-3" v-if="formData.role === 'student'">
              <input type="text" class="form-control" id="fullName" v-model="formData.full_name" placeholder="Full Name" required>
              <label for="fullName">Full Name</label>
            </div>

            <div class="form-floating mb-3" v-if="formData.role === 'company'">
              <input type="text" class="form-control" id="companyName" v-model="formData.company_name" placeholder="Company Name" required>
              <label for="companyName">Company Name</label>
            </div>

            <div class="form-floating mb-3">
              <input type="text" class="form-control" id="regUsername" v-model="formData.username" placeholder="Username" required>
              <label for="regUsername">Username</label>
            </div>

            <div class="form-floating mb-4">
              <input type="password" class="form-control" id="regPassword" v-model="formData.password" placeholder="Password" required>
              <label for="regPassword">Password</label>
            </div>

            <div v-if="errorMessage" class="alert alert-danger py-2"><i class="fa-solid fa-circle-exclamation me-2"></i>{{ errorMessage }}</div>
            <div v-if="successMessage" class="alert alert-success py-2"><i class="fa-solid fa-check-circle me-2"></i>{{ successMessage }}</div>

            <button type="submit" class="btn btn-dark w-100 py-3 rounded-3 fw-bold shadow-sm" :disabled="isLoading">
              <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
              Register
            </button>

            <div class="text-center mt-3">
              <router-link to="/login" class="text-muted text-decoration-none">Already have an account? <span class="text-primary fw-bold">Login</span></router-link>
            </div>
          </form>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RegisterView',
  data() {
    return {
      formData: {
        username: '',
        password: '',
        role: 'student', 
        full_name: '',
        company_name: ''
      },
      errorMessage: "",
      successMessage: "",
      isLoading: false
    }
  },
  methods: {
    registerUser() {
      this.errorMessage = "";
      this.successMessage = "";
      this.isLoading = true;
      const payload = {
        username: this.formData.username,
        password: this.formData.password,
        role: this.formData.role
      };

      if (this.formData.role === 'student') {
        payload.full_name = this.formData.full_name;
      } else if (this.formData.role === 'company') {
        payload.company_name = this.formData.company_name;
      }

      axios.post("http://127.0.0.1:5000/api/register", payload, {
        headers: {
          "Content-Type": "application/json"
        }
      })
      .then(res => {
        this.successMessage = "Registration successful! Redirecting to login...";
        setTimeout(() => {
          this.$router.push('/login');
        }, 1500);
      })
      .catch(err => {
        if (err.response && err.response.status === 409) {
          this.errorMessage = "That username is already taken. Please choose another.";
        } else if (err.response && err.response.data && err.response.data.message) {
          this.errorMessage = err.response.data.message;
        } else {
          this.errorMessage = "Cannot connect to server. Is Flask running?";
        }
      })
      .finally(() => {
        this.isLoading = false;
      })
    }
  }
}
</script>