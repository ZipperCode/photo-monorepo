import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../pages/Home.vue')
    },
    {
      path: '/upload/:code',
      name: 'upload',
      component: () => import('../pages/Upload.vue')
    }
  ]
})

export default router
