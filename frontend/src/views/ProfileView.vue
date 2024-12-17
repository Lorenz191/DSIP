<script setup>

import UserIconBig from "@/components/User/UserIconBig.vue";
import ProfileNav from "@/components/ProfileNav.vue";
import {useRouter} from "vue-router";
import axios from "axios";
import {ref} from "vue";
import {useUserStore} from "@/stores/user.js";

const user = useUserStore()


const router = useRouter();
const posts = ref([])
const sv_posts = ref([])
function backToPostView(){
  router.push({name: 'landing'})
}



const fetchPosts = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/posts/get')
    const sv_response = await axios.get('http://localhost:8000/api/posts_sv/get')
    posts.value = response.data
    sv_posts.value = sv_response.data
  } catch (error) {
    console.error('Error fetching posts:', error)
  } finally {
    loading.value = false
  }
}



</script>

<template>
<div id="header">
  <div id="backArrow-container" @click="backToPostView">
    <img src="../components/icons/arrow_back.svg" alt="arrow_back">
  </div>

</div>

  <div id="icon-container">
    <UserIconBig></UserIconBig>
  </div>

  <div id="nav-container">
    <ProfileNav></ProfileNav>
  </div>

  <div class="post-container">

  </div>
</template>

<style scoped>


#header {
  background: #2EDB7B;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 0 15px;
}
#icon-container {
  margin: 25px;
  display: flex;
  justify-content: center;
}

#backArrow-container {
  display: flex;
  align-items: center;
  cursor: pointer;
}

</style>
