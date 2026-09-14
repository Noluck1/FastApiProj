import type { RouteRecordRaw } from 'vue-router'

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/pages/HomePage/index.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/pages/LoginPage/index.vue'),
  },
  {
    path: '/library/:id(\\d+)',
    name: 'book',
    component: () => import('@/pages/BookPage/index.vue'),
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/pages/RegisterPage/index.vue'),
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/pages/ProfilePage/index.vue'),
  },
]
