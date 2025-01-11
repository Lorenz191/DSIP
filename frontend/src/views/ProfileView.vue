<script setup>
import UserIconBig from '@/components/User/UserIconBig.vue'
import { useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'
import PostRead from '@/components/PostRead.vue'
import axios from 'axios'

const likedP = ref([])
const dislikedP = ref([])
const ownP = ref([])
const states = {
  own: 0,
  like: 1,
  dislike: 2
}

const state = ref(states.own)

const router = useRouter()

function backToPostView() {
  router.push({ name: 'landing' })
}

const toggleownPosts = async () => {
  const response = await axios.get('http://localhost:8000/api/posts/get/user/')
  console.log(response.data)
  ownP.value = response.data
  state.value = states.own
}

const togglelikedPosts = async () => {
  const response = await axios.get('http://localhost:8000/api/posts/get/user/upvoted/')
  console.log(response.data)
  likedP.value = response.data
  state.value = states.like
}

const toggledislikedPosts = async () => {
  const response = await axios.get('http://localhost:8000/api/posts/get/user/downvoted/')
  console.log(response.data)
  dislikedP.value = response.data
  state.value = states.dislike
}

onMounted(() => {
  toggleownPosts()
})
</script>

<template>
  <div id="header">
    <div id="backArrow-container" @click="backToPostView">
      <img src="../components/icons/arrow_back.svg" alt="arrow_back" />
    </div>
  </div>

  <div id="icon-container">
    <UserIconBig></UserIconBig>
  </div>

  <div id="nav-container">
    <div class="nav-container">
      <div
        class="ownPosts-container"
        @click="toggleownPosts"
        :class="{ active: state === states.own }"
      >
        <p>Meine Beiträge</p>
      </div>
      <div
        class="likedPosts-container"
        @click="togglelikedPosts"
        :class="{ active: state === states.like }"
      >
        <p>Gefällt mir</p>
      </div>
      <div
        class="dislikedPosts-container"
        @click="toggledislikedPosts"
        :class="{ active: state === states.dislike }"
      >
        <p>Gefällt mir nicht</p>
      </div>
    </div>
  </div>

  <div class="posts-container">
    <div class="posts-wrapper">
      <template v-if="state === states.own">
        <div class="post-container" v-for="post in ownP" :key="post.id">
          <PostRead :post="post"></PostRead>
        </div>
      </template>

      <template v-else-if="state === states.like">
        <div class="post-container" v-for="post in likedP" :key="post.id">
          <PostRead :post="post"></PostRead>
        </div>
      </template>

      <template v-else-if="state === states.dislike">
        <div class="post-container" v-for="post in dislikedP" :key="post.id">
          <PostRead :post="post"></PostRead>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
#header {
  background: #2edb7b;
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

.nav-container {
  width: 750px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 10px 0;
  margin: 0 auto;
}

.ownPosts-container,
.likedPosts-container,
.dislikedPosts-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px 20px;
  cursor: pointer;
}

.ownPosts-container p,
.likedPosts-container p,
.dislikedPosts-container p {
  margin: 0;
  font-size: 20px;
  font-weight: bold;
}

.ownPosts-container:hover,
.likedPosts-container:hover,
.dislikedPosts-container:hover {
  color: #2edb7b;
  text-decoration: underline;
}

.active {
  color: #2edb7b;
  text-decoration: underline;
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

.posts-container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin-top: 55px;
  min-height: calc(100vh - 80px - 55px);
}
</style>
