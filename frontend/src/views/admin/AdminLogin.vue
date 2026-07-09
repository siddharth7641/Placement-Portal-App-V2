<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        
        <div class="card shadow-lg border-0 bg-dark text-white rounded-4 p-4 mt-5">
          <div class="text-center mb-4 mt-3">
            <i class="fa-solid fa-shield-halved fa-3x text-warning mb-3"></i>
            <h3 class="fw-bold">Admin Portal</h3>
            <p class="text-secondary small">Restricted Access</p>
          </div>

          <form @submit.prevent="loginAdmin">
            
            <div class="form-floating mb-3 text-dark">
              <input type="text" class="form-control" id="adminUsername" v-model="formData.username" placeholder="Admin ID" required>
              <label for="adminUsername"><i class="fa-solid fa-user-shield me-2"></i>Admin Username</label>
            </div>
            
            <div class="form-floating mb-4 text-dark">
              <input type="password" class="form-control" id="adminPassword" v-model="formData.password" placeholder="Password" required>
              <label for="adminPassword"><i class="fa-solid fa-key me-2"></i>Password</label>
            </div>

            <div v-if="error" class="alert alert-danger py-2 border-0" role="alert">
              <i class="fa-solid fa-triangle-exclamation me-2"></i>{{ error }}
            </div>

            <button type="submit" class="btn btn-warning w-100 py-3 rounded-3 fw-bold" :disabled="isLoading">
              <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
              Enter System
            </button>
            
          </form>
        </div>

        <div class="text-center mt-4">
          <router-link to="/login" class="text-muted text-decoration-none small">
            <i class="fa-solid fa-arrow-left me-1"></i> Return to Public Portal
          </router-link>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminLogin',
  data() {
    return {
      formData: {
        username: '',
        password: ''
      },
      error: "",
      isLoading: false
    }
  },
  methods: {
    loginAdmin() {
      this.error = ""
      this.isLoading = true

      axios.post("http://127.0.0.1:5000/api/admin/login", this.formData, {
        headers: { "Content-Type": "application/json" }
      })
      .then(res => {
        localStorage.setItem("access_token", res.data.access_token)
        localStorage.setItem("user_role", res.data.role)
        
        this.$router.push('dashboard')
      })
      .catch(err => {
        if (err.response && err.response.data && err.response.data.message) {
          this.error = err.response.data.message
        } else {
          this.error = "Connection error. Is the server running?"
        }
      })
      .finally(() => {
        this.isLoading = false
      })
    }
  }
}
</script>