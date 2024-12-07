<script setup>
import LandingNav from '@/components/LandingNav.vue'
import axios from 'axios'
import { ref, onMounted } from 'vue'
import PostRead from '@/components/PostRead.vue'
import UserAsideInformaiton from '@/components/User/UserAsideInformaiton.vue'

const posts = ref([])

const fetchPosts = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/posts/get')
    posts.value = response.data
  } catch (error) {
    console.error('Error fetching posts:', error)
  }
}

onMounted(() => {
  fetchPosts()
})
</script>

<template>
  <LandingNav></LandingNav>
  <div class="posts-container">
    <div class="wrapper">
      <div class="aside-container">
        <UserAsideInformaiton></UserAsideInformaiton>
      </div>
      <div class="posts-wrapper">
        <div class="post-container" v-for="post in posts" :key="post.id">
          <PostRead :post="post"></PostRead>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.posts-container {
  width: 80%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 55px;
  gap: 68px;
  min-height: calc(100vh - 80px - 55px);
}

.wrapper {
  display: flex;
  flex-direction: row;
  gap: 200px;
}
</style>
