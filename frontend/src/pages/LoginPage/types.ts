export type LoginFormValues = {
  username: string
  password: string
}

export type TokenResponse = {
  access_token: string
  token_type: string
}

export type UserDto = {
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
