<template>
  <div>
    <h1>Loading...</h1>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuth0 } from '@auth0/auth0-vue'
import { useRouter } from 'vue-router'
import { setSession } from '@/auth/SetSession.js'

const { handleRedirectCallback } = useAuth0()
const router = useRouter()

onMounted(async () => {
  try {
    await handleRedirectCallback()
    console.log('Login completed, setting session...')
    await setSession()
    console.log('Session set, redirecting to target route...')
    const target = window.location.search.split('target=')[1] || '/'
    router.push(target)
  } catch (e) {
    console.error('Error handling redirect callback:', e)
  }
})
</script>
