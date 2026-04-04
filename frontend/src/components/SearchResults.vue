<template>
  <div class="search-results-container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h5 class="text-muted mb-0">
        Search Results for "<span class="text-dark fw-bold">{{ query }}</span>"
      </h5>
      <span class="badge bg-primary rounded-pill">{{ totalResults }} matches</span>
    </div>

    <div v-if="totalResults === 0" class="text-center py-5 mt-4 border rounded bg-white shadow-sm">
      <i class="fa-solid fa-magnifying-glass fa-3x text-muted mb-3 opacity-25"></i>
      <h5 class="text-muted">No matches found for "{{ query }}"</h5>
      <p class="text-muted small">Try checking for typos or using different keywords.</p>
    </div>

    <div v-else class="row">
      <div class="col-md-6 mb-4" v-if="companies.length > 0">
        <h6 class="text-secondary border-bottom pb-2">Organizations ({{ companies.length }})</h6>
        <ul class="list-group shadow-sm">
          <li v-for="company in companies" :key="'src-comp-'+company.id" class="list-group-item d-flex justify-content-between align-items-center border-0 mb-1 rounded">
            <span class="fw-semibold text-dark">{{ company.name }}</span>
            <button @click="$emit('blacklist-company', company.id)" class="btn btn-sm btn-outline-danger px-3 rounded-pill">blacklist</button>
          </li>
        </ul>
      </div>

      <div class="col-md-6 mb-4" v-if="students.length > 0">
        <h6 class="text-secondary border-bottom pb-2">Students ({{ students.length }})</h6>
        <ul class="list-group shadow-sm">
          <li v-for="student in students" :key="'src-stu-'+student.id" class="list-group-item d-flex justify-content-between align-items-center border-0 mb-1 rounded">
            <span class="fw-semibold text-dark">{{ student.name }}</span>
            <button @click="$emit('blacklist-student', student.id)" class="btn btn-sm btn-outline-danger px-3 rounded-pill">blacklist</button>
          </li>
        </ul>
      </div>

      <div class="col-12 mb-4" v-if="drives.length > 0">
        <h6 class="text-secondary border-bottom pb-2">Drives ({{ drives.length }})</h6>
        <div class="table-responsive bg-white rounded shadow-sm">
          <table class="table table-hover mb-0">
            <tbody>
              <tr v-for="drive in drives" :key="'src-drive-'+drive.id">
                <td class="fw-semibold text-dark">{{ drive.name }}</td>
                <td class="text-end">
                  <button @click="$emit('view-drive', drive)" class="btn btn-sm btn-outline-primary rounded-pill px-4">view details</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="col-12 mb-4" v-if="applications.length > 0">
        <h6 class="text-secondary border-bottom pb-2">Applications ({{ applications.length }})</h6>
        <div class="table-responsive bg-white rounded shadow-sm">
          <table class="table table-hover mb-0">
            <tbody>
              <tr v-for="app in applications" :key="'src-app-'+app.id">
                <td><span class="fw-semibold text-dark">{{ app.studentName }}</span> applied to {{ app.companyName }}</td>
                <td class="text-end">
                  <button @click="$emit('view-application', app)" class="btn btn-sm btn-outline-primary rounded-pill px-4">view app</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'SearchResults',
  props: {
    query: String,
    companies: Array,
    students: Array,
    drives: Array,
    applications: Array
  },
  computed: {
    totalResults() {
      return this.companies.length + this.students.length + this.drives.length + this.applications.length;
    }
  }
}
</script>