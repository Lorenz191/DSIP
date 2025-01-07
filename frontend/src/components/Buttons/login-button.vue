<script setup>
import { useAuth0 } from '@auth0/auth0-vue'
const {loginWithRedirect} = useAuth0()

const handleLogin = async () => {
  try {
    console.log('Starting login...');
    await loginWithRedirect({
      appState: { target: '/landing' }
    });
    console.log('Redirecting after login...');
  } catch (error) {
    console.error('Error during login:', error);
  }
};


</script>

<template>
  <button class="button__login" @click="handleLogin">Log In</button>
</template>

<style scoped></style>
