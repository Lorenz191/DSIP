
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './assets/tailwind.css'
import './style.css'
import PrimeVue from 'primevue/config'
import VueNativeSock from 'vue-native-websocket-vue3'


import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue, {
    theme: 'none'
})

app.use(VueNativeSock, 'ws://localhost:8000/ws/votes/', {
    format: 'json',
    reconnection: true,
    reconnectionAttempts: 5,
    reconnectionDelay: 3000,
})

app.mount('#app')
