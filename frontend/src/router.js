import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('./views/Home.vue') 
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('./views/LoginView.vue') 
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('./views/RegisterView.vue')
    },
    {
      path: '/admin/login', 
      name: 'adminLogin',
      component: () => import('./views/admin/AdminLogin.vue')
    },
    {
      path: '/admin',
      component: () => import('./views/admin/AdminLayout.vue'),
      meta: { requiresAuth: true, role: 'admin' },
      children: [
        { 
          path: 'dashboard', 
          name: 'adminDashboard',
          component: () => import('./views/admin/AdminDashboard.vue') 
        },
      ]
    },
    {
      path: '/company',
      component: () => import('./views/company/CompanyLayout.vue'),
      meta: { requiresAuth: true, role: 'company' }, 
      children: [
        { 
          path: 'dashboard', 
          name: 'companyDashboard',
          component: () => import('./views/company/CompanyDashboard.vue') 
        },
        {
          path: 'post-drive',
          name: 'companyPostDrive',
          component: () => import('./views/company/PostDrive.vue')
        },
        {
          path: 'drive/:id/applications',
          name: 'companyDriveApplications',
          component: () => import('./views/company/DriveApplications.vue')
        }
      ]
    },
    {
      path: '/student',
      component: () => import('./views/student/StudentLayout.vue'), // Using the master layout!
      meta: { requiresAuth: true, role: 'student' },
      children: [
        { 
          path: 'dashboard', 
          name: 'studentDashboard',
          component: () => import('./views/student/StudentDashboard.vue') 
        }
      ]
    },
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  const userRole = localStorage.getItem('user_role');

  if (to.meta.requiresAuth) {
    if (!token) {
      return next(to.path.startsWith('/admin') ? '/admin/login' : '/login');
    }
    
    if (to.meta.role && to.meta.role !== userRole) {
      // Direct them to their proper dashboard path
      if (userRole === 'admin') return next('/admin/dashboard');
      return next(`/${userRole}-dashboard`);
    }
  }

  if ((to.name === 'login' || to.name === 'adminLogin') && token) {
    if (userRole === 'admin') return next('/admin/dashboard');
    return next(`/${userRole}-dashboard`);
  }

  next();
})

export default router