<script setup>
import LandingNav from '@/components/LandingNav.vue'
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const post = ref(null)
const loading = ref(true)
const route = useRoute()

const fetchPost = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/post/get/', { 'post_id': route.params.id })
    post.value = response.data
  } catch (error) {
    console.error('Error fetching posts:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchPost()
})
</script>


<template>
  <LandingNav :arrow="true"></LandingNav>

  <div v-if="loading" class="loading-container">
    <span class="loader"> </span>
  </div>

  <div v-else-if="post" class="post-info-container">
    <div class="post-container">
      <div class="date-container">
        <p class="date">Veröffentlicht am {{ new Date(post.created_at).toLocaleDateString() }}</p>
      </div>
      <div class="title-container">
        <h1 class="title">{{ post.body.title }}</h1>
      </div>
      <div class="text-container">
        <p class="post-content">
          {{ post.body.content }}
        </p>
      </div>
    </div>
  </div>

  <div v-else class="error-container">
    <p>Error: Could not fetch post.</p>
  </div>
</template>

<style scoped>
.date {
  color: rgba(51, 51, 51, 0.75);
  font-family: Futura;
  font-size: 13px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
}

.title {
  color: #000;
  font-family: Futura;
  font-size: 32px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
}

.post-content {
  color: #000;
  font-family: Futura;
  font-size: 16px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
}

.post-info-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  margin-top: 90px;
}

.post-container{
  width: 50vw;
}

.title-container{
  margin-bottom: 5px;
}

.loading-container {
  height: 90vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loader {
  width: 84px;
  height: 84px;
  position: relative;
  overflow: hidden;
}

.loader:before, .loader:after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 64px;
  height: 64px;
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

</style>
