<script setup>
import {useRouter} from "vue-router";

const router = new useRouter()


function toProfile() {
  router.push({name: 'profile'})
}
</script>

<template>
<div id="ProfileContainer" @click="toProfile">
  <img  id="ProfilIcon" src="../icons/ProfilIcon.svg" alt="Profil Bild">
</div>
</template>

<style scoped>
#ProfilIcon{
  width: 46px;
  height: 46px;
}
</style>
