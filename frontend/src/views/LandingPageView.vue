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
    <div class="aside-container">
      <UserAsideInformaiton></UserAsideInformaiton>
    </div>
    <div class="posts-wrapper">
      <div class="post-container" v-for="post in posts" :key="post.id">
        <PostRead :post="post"></PostRead>
      </div>
    </div>
    <div class="new-post-container">
      <button class="new-post-button">
        Neuer Beitrag
      </button>
    </div>
  </div>
</template>


<style scoped>
.aside-container, .new-post-container {
  width: 20vw;
}

.posts-container {
  display: flex;
  flex-direction: row;
  margin-top: 55px;
  min-height: calc(100vh - 80px - 55px);
}

.posts-wrapper {
  width: 60vw;
  height: 80vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 16px;
  overflow-y: auto;
  /*box-shadow: 5px 5px 15px 0px rgba(0, 0, 0, 0.25);
  border-radius: 20px;
  border: 3px solid rgba(217, 217, 217, 0.20);*/
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

.new-post-button{
  background: #D9D9D9;
  font-family: Futura;
  font-size: 24px;
  width: 230px;
  height: 40px;
  border-radius: 5px;
}
</style>
