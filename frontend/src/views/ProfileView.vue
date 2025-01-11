<script setup>

import UserIconBig from "@/components/User/UserIconBig.vue";
import {useRouter} from "vue-router";
import {onMounted, onUnmounted, ref} from "vue";
import {useUserStore} from "@/stores/user.js";
import PostRead from "@/components/PostRead.vue";

const user = useUserStore().userUuid;
const likedP = [];
const dislikedP = [];
const ownP = [];
const states = {
  "own": 0,
  "like": 1,
  "dislike": 2
};

const loading = ref(true);


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


const router = useRouter();

function backToPostView(){
  router.push({name: 'landing'})
}

const posts = ref([])
const sv_posts = ref([])

const fetchPosts = async () => {
  try {
    const responsePosts = await fetch('http://localhost:8000/api/posts/get');
    if (!responsePosts.ok) {
      throw new Error('Network response was not ok');
    }
    posts.value = await responsePosts.json();

    fetch('http://localhost:8000/api/posts_sv/get')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    sv_posts.value = data;
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });
    categorisePosts()
  } catch (error) {
    console.error('Error fetching posts:', error)
  } finally {
    loading.value = false
  }
}




function categorisePosts(){

  for (let post of posts.value){
        if(post.fk_author === user){
          ownP.push(post)
        }else if(post.upvotes.includes(user)){
          likedP.push(post)
        }else if(post.downvotes.includes(user)){
          dislikedP.push(post)
        }
  }
}

onMounted(() => {
  fetchPosts()
})


const toggleownPosts = () => {
  state.value = states.own
};

const togglelikedPosts = () => {
    state.value = states.like
};

const toggledislikedPosts = () => {
  state.value = states.dislike
}

</script>

<template>
<div id="header">
  <div id="backArrow-container" @click="backToPostView">
    <img src="../components/icons/Arrow_back.svg" alt="arrow_back">
  </div>

</div>

  <div id="icon-container">
    <UserIconBig></UserIconBig>
  </div>

    <div :class="[{'nav-container' : screenWidth>700}, {'small-nav-container' : screenWidth<700}]" >
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
          <div class="post-container" v-for="post in ownP" :key="post.id">
            <PostRead :post="post"></PostRead>
          </div>
      </div>


      <div v-if="state === 1">
           <div class="post-container" v-for="post in likedP" :key="post.id">
            <PostRead :post="post"></PostRead>
           </div>
      </div>

      <div v-if="state === 2">
           <div class="post-container" v-for="post in dislikedP" :key="post.id">
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
  color: #2EDB7B;
  text-decoration: underline;
}

.active{
  color: #2EDB7B;
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


.small-nav-container {
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
