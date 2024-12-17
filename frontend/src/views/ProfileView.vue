<script setup>

import UserIconBig from "@/components/User/UserIconBig.vue";
import ProfileNav from "@/components/ProfileNav.vue";
import {useRouter} from "vue-router";
import axios from "axios";
import {onMounted, ref} from "vue";
import {useUserStore} from "@/stores/user.js";
import PostRead from "@/components/PostRead.vue";

const user = useUserStore().userUuid;
const own = ref(true);
const liked = ref (false);
const disliked = ref(false);
const likedP = [];
const dislikedP = [];
const ownP = [];


const router = useRouter();
const posts = ref([])
const sv_posts = ref([])
function backToPostView(){
  router.push({name: 'landing'})
}



const fetchPosts = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/posts/get')
    const sv_response = await axios.get('http://localhost:8000/api/posts_sv/get')
    posts.value = response.data
    sv_posts.value = sv_response.data
  } catch (error) {
    console.error('Error fetching posts:', error)
  }finally {
    console.log(posts.value)
    console.log(user)
  }
}

onMounted(() => {
  fetchPosts();
  categorisePosts();
})

function categorisePosts(){
  for (const post of posts.value){
        if(post.value.fk_author.equals(user)){
          ownP.push(post)
        }else if(post.value.upvotes.includes(user)){
          likedP.push(post)
        }else if(post.value.downvotes.includes(user)){
          dislikedP.push(post)
        }
  }
  console.log(ownP);
  console.log(likedP);
  console.log(dislikedP);
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
    <ProfileNav :own="own" :liked="liked" :disliked="disliked" @update:own="own = $event" @update:liked="liked = $event" @update:disliked="disliked = $event"></ProfileNav>
  </div>

  <div class="post-container">
    <template v-if="own">
     <div class="post-container" v-for="post in ownP" :key="post.id">
            <PostRead :post="post"></PostRead>
        </div>
      </template>
    <template v-else-if="liked">
           <div class="post-container" v-for="post in likedP" :key="post.id">
            <PostRead :post="post"></PostRead>
        </div>
    </template>
     <template v-else-if="disliked">
           <div class="post-container" v-for="post in dislikedP" :key="post.id">
            <PostRead :post="post"></PostRead>
        </div>
    </template>

    <template>
    </template>

    <template>

    </template>
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

</style>
