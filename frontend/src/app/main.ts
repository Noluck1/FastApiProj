import { createApp } from 'vue'

import App from '@/App.vue'
import { configureAccessTokenRefresh } from '@/shared/api/http'
import { getCurrentUser, refreshSession } from '@/shared/api/session'
import { useSessionStore } from '@/shared/stores/session.store'
import { useUserStore } from '@/shared/stores/user.store'
import { i18n } from './i18n'
import { pinia } from './pinia'
import router from './router'

import 'vue-sonner/style.css'
import './styles/tailwind.css'
import './styles/index.scss'

const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(i18n)

const sessionStore = useSessionStore(pinia)
const userStore = useUserStore(pinia)
let refreshRequest: Promise<string | null> | null = null

async function refreshAccessToken(): Promise<string | null> {
  if (refreshRequest) {
    return refreshRequest
  }

  refreshRequest = (async () => {
    try {
      const token = await refreshSession()
      sessionStore.setSession(token.access_token, null)
      return token.access_token
    } catch {
      sessionStore.clearSession()
      userStore.clearUser()
      return null
    } finally {
      refreshRequest = null
    }
  })()

  return refreshRequest
}

configureAccessTokenRefresh(refreshAccessToken)

try {
  const accessToken = await refreshAccessToken()

  if (accessToken) {
    userStore.setUser(await getCurrentUser(accessToken))
  }
} catch {
  sessionStore.clearSession()
  userStore.clearUser()
}

app.mount('#app')
