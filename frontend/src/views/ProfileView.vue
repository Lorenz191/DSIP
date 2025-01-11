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


let state = ref(states.own);

const screenWidth = ref(window.innerWidth);

const updateScreenWidth = () => {
  screenWidth.value = window.innerWidth;
};

onMounted(() => {
  window.addEventListener('resize', updateScreenWidth);
});

onUnmounted(() => {
  window.removeEventListener('resize', updateScreenWidth);
});

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


<LandingNav arrow ></LandingNav>

  <div id="icon-container">
    <UserIconBig></UserIconBig>
  </div>


    <div :class="[{'profile-nav-container' : screenWidth>700}, {'profile-small-nav-container' : screenWidth<700}]" >
    <div
      class="ownPosts-container"
      @click="toggleownPosts"
      :class="{ active: (state === 0)}"
    >
      <p>Meine Beiträge</p>
    </div>
    <div
      class="likedPosts-container"
      @click="togglelikedPosts"
      :class="{ active: (state === 1)}"
    >
      <p>Gefällt mir</p>
    </div>
    <div
      class="dislikedPosts-container"
      @click="toggledislikedPosts"
      :class="{ active: state === 2}"
    >
      <p>Gefällt mir nicht</p>
    </div>
  </div>

  <div :class="[{'posts-container' : screenWidth>700}, {'small-posts-container' : screenWidth<700}]">
    <div class="posts-wrapper">

       <div v-if="loading" class="loading-container">
        <span class="loader"> </span>
      </div>

     <div v-if="state === 0">
          <div class="post-container" v-for="post in ownP.values()" :key="post.id">
            <PostRead :post="post"></PostRead>
          </div>
      </div>


      <div v-if="state === 1">
           <div class="post-container" v-for="post in likedP.values()" :key="post.id">
            <PostRead :post="post"></PostRead>
           </div>
      </div>

      <div v-if="state === 2">
           <div class="post-container" v-for="post in dislikedP.values()" :key="post.id">
            <PostRead :post="post"></PostRead>
           </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
#header {
  width: 100%;
  background: #2EDB7B;
  height: 80px;
}

#icon-container {
  margin: 25px;
  display: flex;
  justify-content: center;
}

.profile-nav-container {
  max-width: 750px;
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
  height: 80vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 16px;
  overflow: scroll;
  padding: 16px;
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

.small-posts-container {
  height: calc(100vh - 80px);
  width: auto;
  display: grid;
  grid-template-areas:
  'nav'
  'posts'
  'posts';

  .posts-wrapper {
    height: 75vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    gap: 16px;
    overflow: scroll;
  }

  .posts-wrapper {
    grid-area: posts;
    overflow-x: hidden;
  }

  .post-container {
    width: 90vw;
  }
}


.profile-small-nav-container {
  max-width: 600px;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  margin: 0 auto;
  font-weight: normal;;

  .ownPosts-container p,
  .likedPosts-container p,
  .dislikedPosts-container p {
    font-size: 17px;
    font-weight: bold;
  }
}
</style>
