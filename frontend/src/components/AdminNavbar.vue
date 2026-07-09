<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow">
    <div class="container-fluid px-4">
      
      <router-link class="navbar-brand fw-bold d-flex align-items-center" to="/admin/dashboard">
        <i class="fa-solid fa-shield-halved text-warning me-2 fa-lg"></i>
        <span>Admin Portal</span>
      </router-link>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#adminNavbarContent">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="adminNavbarContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0 ms-lg-3">
          
          <li class="nav-item">
            <router-link class="nav-link" active-class="active fw-bold text-white" to="/admin/dashboard">
              <i class="fa-solid fa-chart-line me-1"></i> Overview
            </router-link>
          </li>

        </ul>

        <div class="d-flex align-items-center mt-3 mt-lg-0">
          <span class="text-light opacity-75 me-4 small d-none d-lg-block">
            <i class="fa-solid fa-user-tie me-1"></i> Logged in as Admin
          </span>
          <button @click="logoutAdmin" class="btn btn-outline-danger btn-sm px-4 rounded-pill fw-bold">
            <i class="fa-solid fa-right-from-bracket me-1"></i> Logout
          </button>
        </div>
      </div>

    </div>
  </nav>
</template>

<script>
export default {
  name: 'AdminNavbar',
  methods: {
    logoutAdmin() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_role')
      this.$router.push('/admin/login')
    }
  }
}
</script>

<style scoped>
.nav-link {
  transition: color 0.2s ease-in-out;
}
.nav-link:hover {
  color: #ffc107 !important; 
}
</style>