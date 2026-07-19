import axios from 'axios'
import type { Course, CourseCreate, CourseUpdate } from '@/types/course'

const baseURL = import.meta.env.VITE_API_HOST
  ? `${import.meta.env.VITE_API_HOST}/api`
  : '/api'

const api = axios.create({ baseURL })

export async function listCourses(): Promise<Course[]> {
  const response = await api.get<Course[]>('/courses')
  return response.data
}

export async function getCourse(id: string): Promise<Course> {
  const response = await api.get<Course>(`/courses/${id}`)
  return response.data
}

export async function createCourse(data: CourseCreate): Promise<Course> {
  const response = await api.post<Course>('/courses', data)
  return response.data
}

export async function updateCourse(id: string, data: CourseUpdate): Promise<Course> {
  const response = await api.put<Course>(`/courses/${id}`, data)
  return response.data
}

export async function deleteCourse(id: string): Promise<void> {
  await api.delete(`/courses/${id}`)
}