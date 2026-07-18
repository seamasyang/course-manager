import { createRouter, createWebHistory } from 'vue-router'
import InstitutionList from '@/views/InstitutionList.vue'

const routes = [
  {
    path: '/',
    redirect: '/institutions',
  },
  {
    path: '/institutions',
    name: 'InstitutionList',
    component: InstitutionList,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router