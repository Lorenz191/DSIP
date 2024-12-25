<script setup>
import LandingNav from '@/components/LandingNav.vue'
import axios from 'axios'
import { ref, onMounted } from 'vue'
import PostRead from '@/components/PostRead.vue'
import UserAsideInformaiton from '@/components/User/UserAsideInformaiton.vue'
import {RouterLink} from "vue-router";
import { useUserStore } from '@/stores/user.js'

const posts = ref([])
const sv_posts = ref([])
const svPosts = ref(false)
const loading = ref(true)
const small = ref(false)

const userID = useUserStore().userUuid
const accessToken = 'YOUR_ACCESS_TOKEN';

const requestOptions = {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  }
};

fetch(`https://${import.meta.env.VITE_AUTH0_DOMAIN}/api/v2/users/${userID}/roles`, requestOptions)
  .then(response => response.json())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

const fetchPosts = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/posts/get')
    const sv_response = await axios.get('http://localhost:8000/api/posts_sv/get')
    posts.value = response.data.sort((a,b) => b.upvotes.length - a.upvotes.length)

    sv_posts.value = sv_response.data
  } catch (error) {
    console.error('Error fetching posts:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchPosts()
})
</script>

<template>
  <LandingNav logout searchbar></LandingNav>
  <div class="posts-container">
    <div class="aside-container">
      <UserAsideInformaiton :sv-posts="svPosts" @update:svPosts="svPosts = $event"></UserAsideInformaiton>
    </div>
    <div class="posts-wrapper">
      <div v-if="loading" class="loading-container">
        <span class="loader"> </span>
      </div>

      <template v-if="!svPosts">
        <div class="post-container" v-for="post in posts" :key="post.id">
            <PostRead :post="post"></PostRead>
        </div>
      </template>
      <template v-else>
        <div class="post-container" v-for="post in sv_posts" :key="post.id">
          <PostRead :post="post"></PostRead>
        </div>
      </template>
    </div>
    <div class="new-post-container"  v-if="!small" >
      <RouterLink :to="`/create`">
      <button class="new-post-button">
        Neuer Beitrag
      </button>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>

.posts-container {
  display: grid;
  grid-template-columns: 1fr 4fr 1fr;
  column-gap: 20px;
  margin-top: 55px;
  min-height: calc(100vh - 80px - 55px);
  width: auto;
}

.posts-wrapper {
  height: 80vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 16px;
  overflow: scroll;
  padding: 16px;
}

.aside-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.new-post-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
}

.new-post-button {
  background: #D9D9D9;
  font-family: Futura;
  font-size: 24px;
  width: 230px;
  height: 40px;
  border-radius: 5px;
  margin-bottom: 60px;
  margin-right: 3vw;
}

.loading-container {
  height: 90vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loader {
  width: 120px;
  height: 120px;
  position: relative;
  overflow: hidden;
}

.loader:before, .loader:after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: #2EDB7B;
  transform: translate(-50%, 100%) scale(0);
  animation: push 2s infinite ease-in;
}

.loader:after {
  animation-delay: 1s;
}

@keyframes push {
  0% {
    transform: translate(-50%, 100%) scale(1);
  }
  15%, 25% {
    transform: translate(-50%, 50%) scale(1);
  }
  50%, 75% {
    transform: translate(-50%, -30%) scale(0.5);
  }
  80%, 100% {
    transform: translate(-50%, -50%) scale(0);
  }
}
input::placeholder{
  font-weight: bolder;
  color: red;
}

</style>
