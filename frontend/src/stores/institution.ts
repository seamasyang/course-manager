import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Institution, InstitutionCreate, InstitutionUpdate } from '@/types/institution'
import * as api from '@/api/institution'

export const useInstitutionStore = defineStore('institution', () => {
  const institutions = ref<Institution[]>([])
  const loading = ref(false)

  async function fetchAll() {
    loading.value = true
    try {
      institutions.value = await api.listInstitutions()
    } finally {
      loading.value = false
    }
  }

  async function create(data: InstitutionCreate): Promise<Institution> {
    const institution = await api.createInstitution(data)
    institutions.value.push(institution)
    return institution
  }

  async function update(id: string, data: InstitutionUpdate): Promise<Institution> {
    const institution = await api.updateInstitution(id, data)
    const index = institutions.value.findIndex((i) => i.id === id)
    if (index !== -1) {
      institutions.value[index] = institution
    }
    return institution
  }

  async function remove(id: string): Promise<void> {
    await api.deleteInstitution(id)
    institutions.value = institutions.value.filter((i) => i.id !== id)
  }

  return { institutions, loading, fetchAll, create, update, remove }
})