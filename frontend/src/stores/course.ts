import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Course, CourseCreate, CourseUpdate } from '@/types/course'
import * as api from '@/api/course'

export const useCourseStore = defineStore('course', () => {
  const courses = ref<Course[]>([])
  const loading = ref(false)

  async function fetchAll() {
    loading.value = true
    try {
      courses.value = await api.listCourses()
    } finally {
      loading.value = false
    }
  }

  async function create(data: CourseCreate): Promise<Course> {
    const course = await api.createCourse(data)
    courses.value.push(course)
    return course
  }

  async function update(id: string, data: CourseUpdate): Promise<Course> {
    const course = await api.updateCourse(id, data)
    const index = courses.value.findIndex((c) => c.id === id)
    if (index !== -1) {
      courses.value[index] = course
    }
    return course
  }

  async function remove(id: string): Promise<void> {
    await api.deleteCourse(id)
    courses.value = courses.value.filter((c) => c.id !== id)
  }

  return { courses, loading, fetchAll, create, update, remove }
})