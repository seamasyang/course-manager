export interface Institution {
  id: string
  name: string
  location: string | null
  contact_name: string | null
  contact_mobile: string | null
  contact_wechat: string | null
}

export interface InstitutionCreate {
  name: string
  location?: string
  contact_name?: string
  contact_mobile?: string
  contact_wechat?: string
}

export interface InstitutionUpdate {
  name?: string
  location?: string
  contact_name?: string
  contact_mobile?: string
  contact_wechat?: string
}