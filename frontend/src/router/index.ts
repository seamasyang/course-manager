import { createRouter, createWebHistory } from 'vue-router'
import InstitutionList from '@/views/InstitutionList.vue'
import ScheduleList from '@/views/ScheduleList.vue'
import CourseList from '@/views/CourseList.vue'

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
  {
    path: '/schedules',
    name: 'ScheduleList',
    component: ScheduleList,
  },
  {
    path: '/courses',
    name: 'CourseList',
    component: CourseList,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router