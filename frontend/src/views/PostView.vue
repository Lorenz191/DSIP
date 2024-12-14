<script setup>
import LandingNav from '@/components/LandingNav.vue'
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const post = ref( [])
const route = useRoute()

const fetchPost = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/post/get/', { "post_id": route.params.id })
    console.log(response.data)
    post.value = response.data
  } catch (error) {
    console.error('Error fetching posts:', error)
  }
}

onMounted(() => {
  fetchPost()
})
</script>

<template>
  <LandingNav></LandingNav>

  <div class="post-info-container">
    <div class="date-container">
      <p class="date">Veröffentlicht am {{ new Date(post.created_at).toLocaleDateString() }}</p>
    </div>
    <div class="title-container">
      <h1 class="title">{{ post.body.title }}</h1>
    </div>
    <div class="text-container">
      <p class="post-content">
        {{post.body.content}}
      </p>
    </div>
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

.post-content{
  color: #000;
  font-family: Futura;
  font-size: 16px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
}
</style>
