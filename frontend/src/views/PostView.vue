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
      <p>
        {{post.body.content}}
      </p>
    </div>
  </div>
</template>

<style scoped>

</style>
