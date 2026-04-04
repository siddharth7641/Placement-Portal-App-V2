<template>
  <div class="d-flex flex-column min-vh-100 bg-light">
    
    <NavBar v-if="!isAdminRoute" />
    
    <main class="flex-grow-1">
      <router-view></router-view>
    </main>
    
    <FooterBar v-if="!isAdminRoute" />
    
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from './components/NavBar.vue'
import FooterBar from './components/FooterBar.vue'

const route = useRoute()

const isAdminRoute = computed(() => {
  return route.path.startsWith('/admin')
})
</script>

<style>
body {
  font-family: 'Poppins', sans-serif;
  background-color: #f4f7f6 !important;
}
.card {
  border-radius: 1rem;
}
</style>