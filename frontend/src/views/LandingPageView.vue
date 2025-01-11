<script setup>
import LandingNav from '@/components/LandingNav.vue'
import axios from 'axios'
import { ref, onMounted, onUnmounted } from 'vue'
import PostRead from '@/components/PostRead.vue'
import { RouterLink } from 'vue-router'
import AsideInformation from '@/components/User/AsideInformation.vue'
import AdminAsideInformation from '@/components/Admin/AdminAsideInformation.vue'
import SVDashboardView from '@/views/SV-DashboardView.vue'
import { useAuth0 } from '@auth0/auth0-vue'
import { setSession } from '@/auth/SetSession.js'
import { useSessionStore } from '@/stores/session.js'

const { isAuthenticated, logout } = useAuth0()
const sessionStore = useSessionStore()
const posts = ref([])
const sv_posts = ref([])
const toDisplay = ref(1)
const loading = ref(true)

const initializeSession = async () => {
  if (!sessionStore.isSessionSet) {
    const isAdmin = await setSession()
    sessionStore.setSessionStatus(true, isAdmin)
  }
}

const fetchUserInfo = async () => {
  try {
    if (isAuthenticated.value === false) {
      logout({
        logoutParams: {
          target: '/'
        }
      })
    }
  } catch (error) {
    console.error('Error fetching user info:', error)
  }
}

const fetchPosts = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/posts/get', { timeout: 10000 })
    const sv_response = await axios.get('http://localhost:8000/api/posts_sv/get', { timeout: 10000 })
    posts.value = response.data.sort((a, b) => b.upvotes.length - a.upvotes.length)
    sv_posts.value = sv_response.data
  } catch (error) {
    console.error('Error fetching posts:', error.message)
  } finally {
    loading.value = false
  }
}

let socket

onMounted(async () => {
  await initializeSession()

  socket = new WebSocket('ws://localhost:8000/ws/posts/')

  socket.onopen = () => {
    console.log('Connected to the Postsocket')
  }

  socket.onmessage = (event) => {
    if (JSON.parse(event.data)['message'] === 'post_delete') {
      fetchPosts()
    }
  }

  socket.onerror = (error) => {
    console.error('Postocket error:', error)
  }

  socket.onclose = (event) => {
    console.log('Postsocket closed:', event)
  }

  await fetchPosts()
  await fetchUserInfo()
})

const screenWidth = ref(window.innerWidth)

const updateScreenWidth = () => {
  screenWidth.value = window.innerWidth
}

onMounted(() => {
  window.addEventListener('resize', updateScreenWidth)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateScreenWidth)
})

const handleSearch = (searchInput) => {
  console.log('Search input:', searchInput)
}
</script>

<template>
  <LandingNav logout searchbar profile-icon @search="handleSearch"></LandingNav>
  <div :class="[{'posts-container' : screenWidth > 700}, {'small-posts-container' : screenWidth < 700}]">

    <div v-if="screenWidth > 700" class="aside-container">
      <AdminAsideInformation v-if="sessionStore.isAdmin"
                             @update:displayChange="toDisplay = $event"></AdminAsideInformation>
      <AsideInformation v-else @update:displayChange="toDisplay = $event"></AsideInformation>
    </div>
    <div v-else class="aside-container-small">
      <AdminAsideInformation :horizontal="true" v-if="sessionStore.isAdmin"
                             @update:displayChange="toDisplay = $event"></AdminAsideInformation>
      <AsideInformation v-else :horizontal="true" @update:displayChange="toDisplay = $event"></AsideInformation>
    </div>

    <div class="posts-wrapper">
      <div v-if="loading" class="loading-container">
        <span class="loader"> </span>
      </div>
      <div v-else>
        <div v-if="toDisplay === 1 && posts.length">
          <div class="post-container" v-for="post in posts" :key="post.id">
            <PostRead :post="post" :adminView="sessionStore.isAdmin"></PostRead>
          </div>
        </div>
        <div v-else-if="toDisplay === 1 && !posts.length">
          <p>No posts available or an error occurred.</p>
        </div>
        <div v-if="toDisplay === 2 && sessionStore.isAdmin">
          <SVDashboardView :posts="posts"></SVDashboardView>
        </div>
        <div v-if="toDisplay === 3">
          <div class="post-container" v-for="post in sv_posts" :key="post.id">
            <PostRead :post="post"></PostRead>
          </div>
        </div>
      </div>
    </div>

    <div class="new-post-container" v-if="!sv_posts.length && screenWidth > 700">
      <RouterLink :to="`/create`">
        <button class="new-post-button">Neuer Beitrag</button>
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

.aside-container-small {
  display: flex;
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
  background: #d9d9d9;
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

.loader:before,
.loader:after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: #2edb7b;
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
  15%,
  25% {
    transform: translate(-50%, 50%) scale(1);
  }
  50%,
  75% {
    transform: translate(-50%, -30%) scale(0.5);
  }
  80%,
  100% {
    transform: translate(-50%, -50%) scale(0);
  }
}

input::placeholder {
  font-weight: bolder;
  color: red;
}

.small-posts-container {
  height: calc(100vh - 80px);
  width: auto;
  display: grid;
  grid-template-areas:
    'posts'
    'posts'
    'aside';

  .posts-wrapper {
    height: 75vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    gap: 16px;
    overflow: scroll;
  }

  .aside-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    height: calc(100vh - 75vh - 80px);
    grid-area: aside;
  }

  .posts-wrapper {
    grid-area: posts;
    overflow-x: hidden;
  }

  .post-container {
    width: 90vw;
  }
}
</style>
