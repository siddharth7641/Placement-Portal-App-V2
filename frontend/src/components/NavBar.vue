<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
    <div class="container">
      <router-link class="navbar-brand fw-bold" to="/">
        <i class="fa-solid fa-graduation-cap me-2 text-primary"></i>Placement Portal
      </router-link>
      
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <template v-if="!isLoggedIn">
            <li class="nav-item">
              <router-link class="nav-link" to="/login">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="btn btn-primary ms-2 rounded-pill px-3" to="/register">Register</router-link>
            </li>
          </template>

          <template v-else>
            <li class="nav-item">
              <router-link class="btn btn-outline-primary rounded-pill px-3 ms-2" :to="`/${userRole}/dashboard`">
                Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <button @click="logout" class="btn btn-outline-danger rounded-pill px-3 ms-2">
                <i class="fa-solid fa-right-from-bracket me-1"></i> Logout
              </button>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const isLoggedIn = ref(false)
const userRole = ref('')
watch(
  () => route.path,
  () => {
    isLoggedIn.value = !!localStorage.getItem('access_token')
    userRole.value = localStorage.getItem('user_role') || 'student'
  },
  { immediate: true } 
)

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user_role')
  isLoggedIn.value = false 
  router.push('/login')
}
</script>