<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="card shadow-lg border-0 overflow-hidden">
          <div class="row g-0">
            
            <div class="col-md-5 bg-primary text-white d-flex flex-column justify-content-center align-items-center p-5">
              <i class="fa-solid fa-rocket fa-4x mb-3"></i>
              <h3 class="fw-bold text-center">Welcome Back!</h3>
              <p class="text-center small opacity-75">Sign in to access your placement dashboard and explore opportunities.</p>
            </div>

            <div class="col-md-7 p-5">
              <h4 class="mb-4 fw-bold text-dark">Account Login</h4>
              
              <form @submit.prevent="loginUser">
                <div class="form-floating mb-3">
                  <input type="text" class="form-control" id="username" v-model="formData.username" placeholder="Username" required>
                  <label for="username"><i class="fa-regular fa-user me-2"></i>Username</label>
                </div>
                
                <div class="form-floating mb-4">
                  <input type="password" class="form-control" id="password" v-model="formData.password" placeholder="Password" required>
                  <label for="password"><i class="fa-solid fa-lock me-2"></i>Password</label>
                </div>

                <div v-if="error" class="alert alert-danger py-2" role="alert">
                  <i class="fa-solid fa-circle-exclamation me-2"></i>{{ error }}
                </div>

                <button type="submit" class="btn btn-primary w-100 py-3 rounded-3 fw-bold shadow-sm" :disabled="isLoading">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                  Sign In
                </button>
                
                <div class="text-center mt-4">
                  <span class="text-muted">Don't have an account? </span>
                  <router-link to="/register" class="text-primary text-decoration-none fw-bold">Register here</router-link>
                </div>
              </form>
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
  name: 'LoginView',
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
    loginUser() {
      this.error = ""
      this.isLoading = true
      axios.post("http://127.0.0.1:5000/api/login", this.formData, {
        headers: {
          "Content-Type": "application/json"
        }
      })
      .then(res => {
        localStorage.setItem("access_token", res.data.access_token)
        localStorage.setItem("user_role", res.data.role)
        this.$router.push(`/${res.data.role}/dashboard`)
      })
      .catch(err => {
        if (err.response && err.response.data && err.response.data.message) {
          this.error = err.response.data.message
        } else {
          this.error = "Cannot connect to server. Is Flask running?"
        }
      })
      .finally(() => {
        this.isLoading = false
      })
    }
  }
}
</script>