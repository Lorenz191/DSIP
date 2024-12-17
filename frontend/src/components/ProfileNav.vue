<script setup>
import {ref} from "vue";

const props = defineProps({
  own:{
    type: Boolean,
    required: true
  },
  liked:{
    type: Boolean,
    required: true,
  },
  disliked:{
    type: Boolean,
    required: true
  }
});
const emit = defineEmits(['update:own','update:liked','update:disliked']);
const activeButton = ref('');



const toggleownPosts = () => {
  emit('update:own', !props.own)
  activeButton.value = 'own';
};

const togglelikedPosts = () => {
    activeButton.value = 'liked';
  emit('update:liked', !props.liked)

};

const toggledislikedPosts = () => {
  activeButton.value = 'disliked';
  emit('update:disliked', !props.disliked)
}


</script>

<template>
  <div class="nav-container">
    <div
      class="ownPosts-container"
      @click="toggleownPosts"
      :class="{ active: activeButton.valueOf() === 'own'}"
    >
      <p>Meine Beiträge</p>
    </div>
    <div
      class="likedPosts-container"
      @click="togglelikedPosts"
      :class="{ active: activeButton.valueOf() === 'liked'}"
    >
      <p>Gefällt mir</p>
    </div>
    <div
      class="dislikedPosts-container"
      @click="toggledislikedPosts"
      :class="{ active: activeButton.valueOf() === 'disliked'}"
    >
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

.active{
  color: #2EDB7B;
  text-decoration: underline;
}








</style>
