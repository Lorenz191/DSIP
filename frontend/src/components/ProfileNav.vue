<script setup>
const props = defineProps({
  own:{
    type: Boolean
  },
  liked:{
    type: Boolean
  },
  disliked:{
    type: Boolean
  }
})




</script>

<template>
<div class="nav-container">
  <div class="ownPosts-container">
    <p>Meine Beiträge</p>
  </div>
  <div class="likedPosts-container">
    <p>Gefällt mir</p>
  </div>
  <div class="dislikedPosts-container">
    <p>Gefällt mir nicht</p>
  </div>
</div>
</template>

<style scoped>

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








</style>
