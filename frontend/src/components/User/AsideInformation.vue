<script setup>
import { ref } from 'vue'

const enumarator = {
  posts: 1,
  svposts: 2
}

const currentState = ref(enumarator.posts)

const emit = defineEmits(['update:displayChange'])

const togglePosts = () => {
  currentState.value = enumarator.posts
  emit('update:displayChange', 1)
}

const toggleSv = () => {
  currentState.value = enumarator.svposts
  emit('update:displayChange', 2)
}
</script>

<template>
  <div class="aside-container">
    <div class="top-container" :class="{ clicked: currentState === 1 }" @click="togglePosts">
      <img src="../icons/Chat_Bubbles.svg" alt="Chat Bubbles" class="chat-icon" />
    </div>
    <div class="seperation-container">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="100px"
        height="5"
        viewBox="0 0 69 5"
        fill="none"
        id="line"
      >
        <path
          d="M2.7037 2.80457H66.2963"
          stroke="#6FD1DE"
          stroke-opacity="0.85"
          stroke-width="4"
          stroke-linecap="round"
          class="separation-line"
          :class="{
            posts: currentState === 1,
            svposts: currentState === 2
          }"
        />
      </svg>
    </div>

    <div class="bottom-container" :class="{ clicked: currentState === 2 }" @click="toggleSv">
      <img src="../icons/Megaphone.svg" alt="Megaphone" class="megaphone" />
    </div>
  </div>
</template>

<style scoped>
.aside-container {
  width: 100px;
  height: 240px;
}

.top-container,
.bottom-container {
  width: 100px;
  height: 120px;
}

.top-container {
  border-radius: 30px 30px 0px 0px;
  border-top: 2px solid rgba(221, 221, 221, 0.87);
  border-right: 2px solid rgba(221, 221, 221, 0.87);
  border-left: 2px solid rgba(221, 221, 221, 0.87);
  background: #fff;
}

.bottom-container {
  border-radius: 0px 0px 30px 30px;
  border-bottom: 2px solid rgba(221, 221, 221, 0.87);
  border-right: 2px solid rgba(221, 221, 221, 0.87);
  border-left: 2px solid rgba(221, 221, 221, 0.87);
  background: #fff;
}

.bottom-container,
.top-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.megaphone,
.chat-icon {
  width: 60px;
}

.bottom-container:hover,
.top-container:hover {
  cursor: pointer;
}

.bottom-container.clicked {
  border-bottom: 5px solid #2edb7b;
  border-right: 5px solid #2edb7b;
  border-left: 5px solid #2edb7b;
}

.top-container.clicked {
  border-top: 5px solid rgba(111, 209, 222, 0.85);
  border-right: 5px solid rgba(111, 209, 222, 0.85);
  border-left: 5px solid rgba(111, 209, 222, 0.85);
}

.separation-line.posts {
  stroke: #6FD1DE;
}

.separation-line.svposts {
  stroke: #2EDB7B;
}
</style>
