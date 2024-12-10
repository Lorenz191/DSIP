<script setup>

import UserIconBig from "@/components/User/UserIconBig.vue";
import ProfileNav from "@/components/ProfileNav.vue";
import {useRouter} from "vue-router";
const router = useRouter()
function backToPostView(){
  router.push({name: 'landing'})
}
</script>

<template>
<div id="header">
  <div id="backArrow-container" @click="backToPostView">
    <img src="../components/icons/arrow_back.svg" alt="arrow_back">
  </div>

</div>

  <div id="ProfileContainer">
    <UserIconBig></UserIconBig>
    <ProfileNav></ProfileNav>

  </div>
</template>

<style scoped>


#header {
  background: #2EDB7B;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 0 16px;
}

#backArrow-container {
  display: flex;
  align-items: center;
  cursor: pointer;
}

</style>
