/**
 * plugins/index.ts
 *
 * Automatically included in `./src/main.ts`
 */
// Types
import type { App } from 'vue'

// Plugins
import router from '../router'
import pinia from '../stores'
import i18n from './i18n'
import vuetify from './vuetify'

export function registerPlugins (app: App) {
  app
    .use(vuetify)
    .use(pinia)
    .use(i18n)
    .use(router)
}
