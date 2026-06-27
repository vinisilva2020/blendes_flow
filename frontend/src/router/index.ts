import { createRouter, createWebHistory } from 'vue-router'

import { useAuthenticationStore } from '@/stores/authentication'
import { useWorkspaceStore } from '@/stores/workspace'

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
      meta: {
        guestOnly: true,
      },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue'),
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('../views/auth/ResetPassword.vue'),
    },
    {
      path: '/confirm-otp',
      name: 'confirm-otp',
      component: () => import('../views/auth/ConfirmOTPView.vue'),
    },
    {
      path: '/new-password',
      name: 'new-password',
      component: () => import('../views/auth/NewPasswordView.vue'),
    },
    {
      path: '/organizations',
      name: 'organizations',
      alias: ['/organization', '/workspace', '/workspaces'],
      component: () => import('../views/organizations/OrganizationsView.vue'),
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/dashboard',
      component: () => import('../layouts/DashboardLayout.vue'),
      meta: {
        requiresAuth: true,
        requiresWorkspace: true,
      },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: () => import('../views/dashboard/Index.vue'),
          meta: {
            headerAvatarLabel: 'BF',
            headerSubtitle: 'Monitor your workspace, active flows, and recent collaboration.',
            headerTitle: 'Dashboard',
          },
        },
        {
          path: 'workflows',
          name: 'dashboard-workflows',
          component: () => import('../views/dashboard/Workflows.vue'),
          meta: {
            headerAvatarLabel: 'WF',
            headerSubtitle: 'Build and refine the flow canvas for your team processes.',
            headerTitle: 'Workflows',
          },
        },
        {
          path: 'settings',
          name: 'dashboard-settings',
          component: () => import('../views/dashboard/Settings.vue'),
          meta: {
            headerAvatarLabel: 'ST',
            headerSubtitle: 'Manage your account preferences and application settings.',
            headerTitle: 'Settings',
          },
        },
        {
          path: 'profile',
          name: 'dashboard-profile',
          component: () => import('../views/dashboard/Profile.vue'),
          meta: {
            headerAvatarLabel: 'PR',
            headerSubtitle: 'View and edit your personal profile information.',
            headerTitle: 'Profile',
          },
        },
      ],
    },
  ],
})

router.beforeEach((to) => {
  const authenticationStore = useAuthenticationStore()
  const workspaceStore = useWorkspaceStore()
  const requiresAuth = to.matched.some((route) => route.meta.requiresAuth)
  const requiresWorkspace = to.matched.some((route) => route.meta.requiresWorkspace)
  const guestOnly = to.matched.some((route) => route.meta.guestOnly)

  if (requiresAuth && !authenticationStore.isAuthenticated) {
    return {
      name: 'auth',
      query: {
        redirect: to.fullPath,
      },
    }
  }

  if (guestOnly && authenticationStore.isAuthenticated) {
    return { name: 'organizations' }
  }

  if (requiresWorkspace && !workspaceStore.hasWorkspace) {
    return { name: 'organizations' }
  }
})

export default router
