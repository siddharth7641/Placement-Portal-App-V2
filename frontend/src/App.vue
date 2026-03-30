<template>
  <div class="d-flex flex-column min-vh-100 bg-light">
    <NavBar />
    
    <main class="flex-grow-1">
      <router-view></router-view>
    </main>
    
    <FooterBar />
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue'
import FooterBar from './components/FooterBar.vue'
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