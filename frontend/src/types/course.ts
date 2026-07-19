export interface Course {
  id: string
  schedule_id: string
  date: string | null
  content: string | null
  follow_up: string | null
}

export interface CourseCreate {
  schedule_id: string
  date?: string
  content?: string
  follow_up?: string
}

export interface CourseUpdate {
  schedule_id?: string
  date?: string
  content?: string
  follow_up?: string
}