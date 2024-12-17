<script setup>

import LandingNav from "@/components/LandingNav.vue";
</script>

<template>
  <LandingNav :arrow="true" :searchbar="false"></LandingNav>
  <div class="header">
    <h1>Neuen Beitrag erstellen</h1>
  </div>
  <div class="content">
    <input type="text" placeholder="Titel">
  </div>
</template>

<style scoped>
  .content{
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>
