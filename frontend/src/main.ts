import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import { installServerState } from './lib/query/install'
import router from './router'
import { useAuthenticationStore } from './stores/authentication'
import { useWorkspaceStore } from './stores/workspace'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
installServerState(app)

const authenticationStore = useAuthenticationStore(pinia)
const workspaceStore = useWorkspaceStore(pinia)

authenticationStore
  .restoreSession()
  .then((isSessionRestored) => {
    if (!isSessionRestored) {
      workspaceStore.clearWorkspace()
    }
  })
  .finally(() => {
    app.use(router)
    app.mount('#app')
  })
