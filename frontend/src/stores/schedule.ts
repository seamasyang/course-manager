import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Schedule, ScheduleCreate, ScheduleUpdate } from '@/types/schedule'
import * as api from '@/api/schedule'

export const useScheduleStore = defineStore('schedule', () => {
  const schedules = ref<Schedule[]>([])
  const loading = ref(false)

  async function fetchAll() {
    loading.value = true
    try {
      schedules.value = await api.listSchedules()
    } finally {
      loading.value = false
    }
  }

  async function create(data: ScheduleCreate): Promise<Schedule> {
    const schedule = await api.createSchedule(data)
    schedules.value.push(schedule)
    return schedule
  }

  async function update(id: string, data: ScheduleUpdate): Promise<Schedule> {
    const schedule = await api.updateSchedule(id, data)
    const index = schedules.value.findIndex((s) => s.id === id)
    if (index !== -1) {
      schedules.value[index] = schedule
    }
    return schedule
  }

  async function remove(id: string): Promise<void> {
    await api.deleteSchedule(id)
    schedules.value = schedules.value.filter((s) => s.id !== id)
  }

  return { schedules, loading, fetchAll, create, update, remove }
})