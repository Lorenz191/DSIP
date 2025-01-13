<script setup>
import { useAuth0 } from '@auth0/auth0-vue'

const { loginWithRedirect } = useAuth0()

const handleLogin = async () => {
  try {
    console.log('Starting login...')
    await loginWithRedirect({
      appState: { target: '/landing' }
    })
    console.log('Redirecting after login...')
  } catch (error) {
    console.error('Error during login:', error)
  }
}
</script>

<template>
  <button class="button__login" @click="handleLogin">Anmelden</button>
</template>

<style scoped>
button {
  color: white;
  font-family: Futura;
  font-weight: bold;
  background: #2edb7b;
  padding: 10px;
  border-radius: 5px;
}

button:hover {
  cursor: pointer;
  background: #1e9e57;
}
</style>
