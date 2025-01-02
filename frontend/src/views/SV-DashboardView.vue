<script setup>
import PostRead from '@/components/PostRead.vue'

const props = defineProps({
  posts: {
    type: Array,
    required: true
  }
})

const totalPostCount = props.posts.length
const month = new Date().getMonth()

const postCountMonth = props.posts.filter((post) => {
  const postMonts = new Date(post.created_at).getMonth()
  return postMonts === month
}).length

const bestPosts = props.posts.sort((a,b) => b.upvotes.length - a.upvotes.length).slice(0, 5)

const worstPosts = props.posts.sort((a,b) => b.downvotes.length - a.downvotes.length).slice(0, 5)

</script>

<template>
  <div class="count-container">
    <div class="total-count-container">
      <p class="count">{{ totalPostCount }}</p>
      <p class="description">Posts veröffentlicht</p>
    </div>
    <div class="monthly-count-container">
      <p class="count">{{ postCountMonth }}</p>
      <p class="description">Posts diesen Monat veröffentlicht</p>
    </div>
  </div>
  <div class="post-container">
    <div class="best-post-container">
      <div class="post-container" v-for="post in bestPosts">
        <PostRead :post="post" :admin-view="true"></PostRead>
      </div>
    </div>
    <div class="worst-post-container">

    </div>
  </div>
</template>

<style scoped>
.count-container{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10vh;
  margin-bottom: 10vh;
}

.total-count-container, .monthly-count-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: fit-content;
  padding-left: 5vh;
  padding-right: 5vh;
  border-radius: 20px;
  border-top: 5px solid #2e5adb;
  background: #fff;
  box-shadow: 0px 4px 4px 0px rgba(0, 0, 0, 0.25);
}

p {
  font-family: Futura;
}

.count {
  font-size: 36px;
}

.description {
  font-size: 27px;
}

.best-post-container, .worst-post-container {
  max-height: 50vh;
  width: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 5vh;
}



</style>
