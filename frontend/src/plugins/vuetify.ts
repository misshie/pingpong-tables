/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Composables
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

const myCustomLightTheme = {
  dark: false,
  colors: {
    'background': '#FFFFFF',
    'surface': '#FFFFFF',
    'primary': '#6200EE',
    'primary-darken-1': '#3700B3',

    'secondary': '#03DAC6',
    'secondary-darken-1': '#018786',
    'error': '#B00020',
    'info': '#2196F3',
    'success': '#4CAF50',
    'warning': '#FB8C00',

    'tertiary': '#C13E1E',
    'tertiary-darken-1': '#832b15ff',
  },
}

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: myCustomLightTheme,
    },
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
})
