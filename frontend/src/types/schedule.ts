export interface Schedule {
  id: string
  institution_id: string
  subject: string
  teacher_name: string | null
  start_date: string | null
  end_date: string | null
  start_time: string | null
  end_time: string | null
  remarks: string | null
}

export interface ScheduleCreate {
  institution_id: string
  subject: string
  teacher_name?: string
  start_date?: string
  end_date?: string
  start_time?: string
  end_time?: string
  remarks?: string
}

export interface ScheduleUpdate {
  institution_id?: string
  subject?: string
  teacher_name?: string
  start_date?: string
  end_date?: string
  start_time?: string
  end_time?: string
  remarks?: string
}