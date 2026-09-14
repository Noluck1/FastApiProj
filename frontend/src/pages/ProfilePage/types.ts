export type ProfileFormValues = {
  firstName: string
  lastName: string
  middleName: string
}

export type UpdateFullNamePayload = {
  first_name: string
  last_name: string
  middle_name: string | null
}

export type ApiResponse<T> = {
  status: 'success' | 'error'
  message: string
  data: T | null
}
