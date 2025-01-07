<script setup>

import UserIconBig from "@/components/User/UserIconBig.vue";
import ProfileNav from "@/components/ProfileNav.vue";
import {useRouter} from "vue-router";
import {onMounted, ref} from "vue";
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

let state = ref(states.own);




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

    //console.log(posts.value[0])
    //console.log(sv_posts)
    categorisePosts()
  } catch (error) {
    console.error('Error fetching posts:', error)
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
  console.log(ownP);
  console.log(likedP);
  console.log(dislikedP);
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
    <img src="../components/icons/arrow_back.svg" alt="arrow_back">
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
  </div>

  <div class="posts-container">
    <div class="posts-wrapper">
     <template v-if="state === 0">
     <div class="post-container" v-for="post in ownP" :key="post.id">
            <PostRead :post="post"></PostRead>
        </div>
      </template>

      <template v-else-if="state === 1">
           <div class="post-container" v-for="post in likedP" :key="post.id">
            <PostRead :post="post"></PostRead>
        </div>
      </template>

      <template v-else-if="state === 2">
           <div class="post-container" v-for="post in dislikedP" :key="post.id">
            <PostRead :post="post"></PostRead>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>

#header {
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
  color: #2EDB7B;
  text-decoration: underline;
}

.active{
  color: #2EDB7B;
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
  margin-top: 55px;
  min-height: calc(100vh - 80px - 55px);
}

</style>
