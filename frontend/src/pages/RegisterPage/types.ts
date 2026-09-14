export type RegisterFormValues = {
  username: string
  password: string
  confirmPassword: string
}

export type RegisterCredentials = Pick<RegisterFormValues, 'username' | 'password'>

export type RegisteredUser = {
  id: number
  username: string
  role: 'user' | 'author' | 'admin'
  is_active: boolean
}

export type ApiResponse<T> = {
  status: 'success' | 'error'
  message: string
  data: T | null
}
