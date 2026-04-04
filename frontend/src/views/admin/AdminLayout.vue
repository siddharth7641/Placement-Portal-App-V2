<template>
  <div class="admin-layout-wrapper bg-light min-vh-100">
    <AdminNavbar />

    <main class="py-4">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import AdminNavbar from '../../components/AdminNavbar.vue'

export default {
  name: 'AdminLayout',
  components: {
    AdminNavbar
  }
}
</script>