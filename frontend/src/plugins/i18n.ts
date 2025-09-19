/* eslint-disable perfectionist/sort-imports */
import { createI18n } from 'vue-i18n'
import pinia from '../stores' // Import the created Pinia instance
import { useStore } from '@/stores/app'

// Import all locale message files
import de from '@/locales/de.json'
import en from '@/locales/en-US.json'
import es from '@/locales/es.json'
import fr from '@/locales/fr.json'
import it from '@/locales/it.json'
import ja from '@/locales/ja.json'
import ko from '@/locales/ko.json'
import ptBR from '@/locales/pt-BR.json'
import zhCN from '@/locales/zh-CN.json'
import zhTW from '@/locales/zh-TW.json'

// This allows using the store before app.use(pinia) is called.
const store = useStore(pinia)

const i18n = createI18n({
  legacy: false,
  locale: store.locale, // Set initial locale from Pinia store
  fallbackLocale: 'en-US', // Set fallback locale
  messages: {
    // Locales are ordered with en-US first, then alphabetically
    'en-US':
    en,
    de,
    es,
    fr,
    it,
    ja,
    ko,
    'pt-BR': ptBR,
    'zh-CN': zhCN,
    'zh-TW': zhTW,
  },
})

export default i18n
