import './assets/main.css'

import posthog from 'posthog-js'
import { createApp } from 'vue'
import App from './App.vue'

posthog.init('phc_vmyGKk9d2D9GzpJZH6p5YWW67cP4Qnndt2miMWejurwi', {
  api_host: 'https://pineapple.byvova.com',
  defaults: '2026-05-30'
})
posthog.register({ project: 'potato' })

createApp(App).mount('#app')
