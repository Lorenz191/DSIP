<script setup>
import { ref, onMounted } from 'vue'
import AuthService from './auth/AuthService'

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


onMounted(() => {
  handleAuthentication()

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
      @click="logout"
    >
      Log Out
    </button>

    {{ message }}
    <br />
  </div>
</template>
