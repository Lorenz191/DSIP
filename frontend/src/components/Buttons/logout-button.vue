<script setup>
 import {useAuth0} from '@auth0/auth0-vue';
 const { logout } = useAuth0();

 const handleLogOut = () => {
   logout({
     logoutParams: {
       target:'/',
     }
   })
 }
</script>

<template>
  <button class="button__logout" @click="handleLogOut">Log Out</button>
</template>

<style scoped>

</style>
