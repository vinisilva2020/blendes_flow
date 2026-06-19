import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/landing_page/HomeView.vue'),
    },
    {
      path: '/auth',
      name: 'auth',
      component: () => import('../views/auth/AuthView.vue'), 
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue'),
    },
    {
      path: '/organizations',
      name: 'organizations',
      component: () => import('../views/organizations/OrganizationView.vue'),
    },
    {
      path: '/canvas',
      name: 'canvas',
      component: () => import('../views/canvas/CanvasView.vue'),
    },
  ],
})

export default router
