import axios from 'axios'
import type { Schedule, ScheduleCreate, ScheduleUpdate } from '@/types/schedule'

const baseURL = import.meta.env.VITE_API_HOST
  ? `${import.meta.env.VITE_API_HOST}/api`
  : '/api'

const api = axios.create({ baseURL })

export async function listSchedules(): Promise<Schedule[]> {
  const response = await api.get<Schedule[]>('/schedules')
  return response.data
}

export async function getSchedule(id: string): Promise<Schedule> {
  const response = await api.get<Schedule>(`/schedules/${id}`)
  return response.data
}

export async function createSchedule(data: ScheduleCreate): Promise<Schedule> {
  const response = await api.post<Schedule>('/schedules', data)
  return response.data
}

export async function updateSchedule(id: string, data: ScheduleUpdate): Promise<Schedule> {
  const response = await api.put<Schedule>(`/schedules/${id}`, data)
  return response.data
}

export async function deleteSchedule(id: string): Promise<void> {
  await api.delete(`/schedules/${id}`)
}