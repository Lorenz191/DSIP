import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './assets/tailwind.css'
import './style.css'
import 'vue-toastification/dist/index.css';
import PrimeVue from 'primevue/config'
import VueNativeSock from 'vue-native-websocket-vue3'
import Toast from "vue-toastification";

import App from './App.vue'
import router from './router'
import { createAuth0 } from '@auth0/auth0-vue'

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

app.use(
  createAuth0({
      domain: import.meta.env.VITE_AUTH0_DOMAIN,
      clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
      authorizationParams: {
          redirect_uri: window.location.origin + '/callback',
      },
  })
)

app.use(Toast, {
  transition: "Vue-Toastification__fade",
  maxToasts: 20,
  newestOnTop: true,
})

app.mount('#app')
