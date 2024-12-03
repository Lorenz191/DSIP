<script setup>
import { ref, onMounted } from 'vue'
import AuthService from './auth/AuthService'
import axios from 'axios'

const API_URL = 'http://localhost:8000'
const auth = new AuthService()

const authenticated = ref(false)
const message = ref('')
const userProfile = ref(null)

const handleAuthentication = () => {
  auth.handleAuthentication()
}

const login = () => {
  auth.login()
}

const logout = () => {
  auth.logout()
}

const privateMessage = async () => {
  const url = `${API_URL}/api/private/`
  try {
    const response = await axios.get(url, {
      headers: { Authorization: `Bearer ${auth.getAuthToken()}` }
    })
    message.value = response.data || ''
  } catch (error) {
    console.error('Error fetching private message:', error)
    message.value = 'Error fetching private message.'
  }
}

onMounted(() => {
  // Handle authentication on mount
  handleAuthentication()

  // Listen for authentication state changes
  auth.authNotifier.on('authChange', (authState) => {
    authenticated.value = authState.authenticated
    if (authState.authenticated) {
      userProfile.value = auth.getUserProfile()
      message.value = userProfile.value ? `Hello, ${userProfile.value.name}` : 'User authenticated'
    } else {
      userProfile.value = null
      message.value = ''
    }
  })

  // Initialize authentication status
  authenticated.value = auth.isAuthenticated()
  if (authenticated.value) {
    userProfile.value = auth.getUserProfile()
    message.value = userProfile.value ? `Hello, ${userProfile.value.name}` : ''
  }
})
</script>

<template>
  <div>
    <button
      class="btn btn-primary btn-margin"
      v-if="!authenticated"
      @click="login"
    >
      Log In
    </button>

    <button
      class="btn btn-primary btn-margin"
      v-if="authenticated"
      @click="privateMessage"
    >
      Call Private
    </button>

    <button
      class="btn btn-primary btn-margin"
      v-if="authenticated"
      @click="logout"
    >
      Log Out
    </button>

    {{ message }}
    <br />
  </div>
</template>
