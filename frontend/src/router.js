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
      path: '/admin',
      name: 'adminLogin',
      component: () => import('./views/AdminLogin.vue')
    },
    // {
    //   path: '/admin-dashboard',
    //   name: 'admin',
    //   component: () => import('./views/AdminDashboard.vue'),
    //   meta: { requiresAuth: true, role: 'admin' }
    // },
    // {
    //   path: '/student-dashboard',
    //   name: 'student',
    //   component: () => import('./views/StudentDashboard.vue'),
    //   meta: { requiresAuth: true, role: 'student' }
    // },
    // {
    //   path: '/company-dashboard',
    //   name: 'company',
    //   component: () => import('./views/CompanyDashboard.vue'),
    //   meta: { requiresAuth: true, role: 'company' }
    // }
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  const userRole = localStorage.getItem('user_role');

  if (to.meta.requiresAuth) {
    if (!token) {
      return next('/login');
    }
    if (to.meta.role && to.meta.role !== userRole) {
      return next(`/${userRole}-dashboard`);
    }
  }

  if (to.name === 'login' && token) {
    return next(`/${userRole}-dashboard`);
  }

  next();
})

export default router