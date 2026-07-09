<template>
  <div class="home-wrapper">
    <section class="bg-primary text-white text-center py-5 shadow-sm">
      <div class="container py-5">
        <div class="row justify-content-center">
          <div class="col-lg-8">
            <h1 class="display-4 fw-bold mb-3">Welcome to the Placement Portal</h1>
            <p class="lead mb-4 opacity-75">
              Bridging the gap between top-tier talent and industry-leading companies. 
              Manage placement drives, track applications, and launch your career all in one place.
            </p>
            <div class="d-flex justify-content-center gap-3">
              <router-link to="/register" class="btn btn-light btn-lg px-4 rounded-pill fw-bold text-primary shadow-sm">
                Get Started
              </router-link>
              <router-link to="/login" class="btn btn-outline-light btn-lg px-4 rounded-pill fw-bold">
                Login
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="container py-5 mt-4 mb-5">
      <div class="text-center mb-5">
        <h2 class="fw-bold">How It Works</h2>
        <p class="text-muted">A unified platform for all your placement needs.</p>
      </div>

      <div class="row g-4">
        <div class="col-md-4">
          <div class="card h-100 border-0 shadow-sm text-center p-4">
            <div class="card-body">
              <div class="mb-3">
                <i class="fa-solid fa-user-graduate fa-3x text-primary"></i>
              </div>
              <h4 class="fw-bold">For Students</h4>
              <p class="text-muted">
                Create your profile, upload your resume, and seamlessly apply to placement drives from top companies. Track your application status in real-time.
              </p>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card h-100 border-0 shadow-sm text-center p-4">
            <div class="card-body">
              <div class="mb-3">
                <i class="fa-solid fa-building fa-3x text-success"></i>
              </div>
              <h4 class="fw-bold">For Companies</h4>
              <p class="text-muted">
                Post job openings, schedule placement drives, and filter through a pool of talented students. Shortlist and hire the best candidates effortlessly.
              </p>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card h-100 border-0 shadow-sm text-center p-4">
            <div class="card-body">
              <div class="mb-3">
                <i class="fa-solid fa-university fa-3x text-warning"></i>
              </div>
              <h4 class="fw-bold">For Institutes</h4>
              <p class="text-muted">
                Maintain complete control over the placement process. Approve company registrations, monitor student statistics, and generate detailed reports.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="bg-dark text-white text-center py-5">
      <div class="container">
        <h3 class="fw-bold mb-3">Ready to kickstart the recruitment process?</h3>
        <router-link to="/register" class="btn btn-primary btn-lg rounded-pill px-5 mt-2">
          Join the Portal Today
        </router-link>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.card {
  transition: transform 0.2s ease-in-out;
}
.card:hover {
  transform: translateY(-5px);
}
</style>