<script setup>
import LandingNav from '@/components/LandingNav.vue'
import axios from 'axios'
import { ref, onMounted } from 'vue'
import PostRead from '@/components/PostRead.vue'
import UserAsideInformaiton from '@/components/User/UserAsideInformaiton.vue'
import CreatePostModal from "@/components/CreatePostModal.vue";

const posts = ref([])
const sv_posts = ref([])
const svPosts = ref(false)

const showModal = ref(false)
const openCreatePostModal = () => {
  showModal.value = true
}

const closeCreatePostModal = () => {
  showModal.value = false
  fetchPosts()
}


const fetchPosts = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/posts/get')
    const sv_response = await axios.get('http://localhost:8000/api/posts_sv/get')
    posts.value = response.data
    sv_posts.value = sv_response.data
  } catch (error) {
    console.error('Error fetching posts:', error)
  }
}

onMounted(() => {
  fetchPosts()
})
</script>

<template>
  <LandingNav logout></LandingNav>
  <div class="posts-container">
    <div class="aside-container">
      <UserAsideInformaiton :sv-posts="svPosts" @update:svPosts="svPosts = $event"></UserAsideInformaiton>
    </div>
    <div class="posts-wrapper">
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
    <div class="new-post-container">
      <button @click="openCreatePostModal" class="new-post-button">
        Neuer Beitrag
      </button>
    </div>
  </div>

  <div v-if="showModal" class="modal-overlay">
    <CreatePostModal @close="closeCreatePostModal"></CreatePostModal>
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
}

/* Overlay for the modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

</style>
