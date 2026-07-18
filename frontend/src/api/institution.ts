import axios from 'axios'
import type { Institution, InstitutionCreate, InstitutionUpdate } from '@/types/institution'

const api = axios.create({
  baseURL: '/api',
})

export async function listInstitutions(): Promise<Institution[]> {
  const response = await api.get<Institution[]>('/institutions/')
  return response.data
}

export async function getInstitution(id: string): Promise<Institution> {
  const response = await api.get<Institution>(`/institutions/${id}`)
  return response.data
}

export async function createInstitution(data: InstitutionCreate): Promise<Institution> {
  const response = await api.post<Institution>('/institutions/', data)
  return response.data
}

export async function updateInstitution(id: string, data: InstitutionUpdate): Promise<Institution> {
  const response = await api.put<Institution>(`/institutions/${id}`, data)
  return response.data
}

export async function deleteInstitution(id: string): Promise<void> {
  await api.delete(`/institutions/${id}`)
}