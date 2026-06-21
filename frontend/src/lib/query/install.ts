import { VueQueryPlugin } from '@tanstack/vue-query'
import type { App } from 'vue'

import { queryClient } from './client'

export function installServerState(app: App) {
  app.use(VueQueryPlugin, { queryClient })
}
