<script setup>
import { ref } from 'vue'

const emit = defineEmits(['update:displayChange'])

const enumarator = {
  posts: 1,
  adminstat: 2,
  svposts: 3
}

const currentState = ref(enumarator.posts)

const togglePost = () => {
  currentState.value = enumarator.posts
  emit('update:displayChange', 1)
}

const toggleAdmin = () => {
  currentState.value = enumarator.adminstat
  emit('update:displayChange', 2)
}

const toggleSvPosts = () => {
  currentState.value = enumarator.svposts
  emit('update:displayChange', 3)
}

</script>

<template>
  <div class="aside-container">
    <div class="top-container" :class="{ clicked: currentState === 1 }" @click="togglePost">
      <img src="../icons/Chat_Bubbles.svg" alt="Chat Bubbles" class="chat-icon" />
    </div>

    <div class="separation-container">
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
            adminstat: currentState === 2,
            svposts: currentState === 3
          }"
        />
      </svg>
    </div>

    <div class="admin-container" :class="{ clicked: currentState === 2 }" @click="toggleAdmin">
      <img src="../icons/Statistic.svg" alt="Statistic Icon" class="statistic-icon" />
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
            adminstat: currentState === 2,
            svposts: currentState === 3
          }"
        />
      </svg>
    </div>

    <div class="bottom-container" :class="{ clicked: currentState === 3 }" @click="toggleSvPosts">
      <img src="../icons/Megaphone.svg" alt="Megaphone" class="megaphone" />
    </div>
  </div>
</template>

<style scoped>
.aside-container {
  width: 100px;
  height: 360px;
}

.top-container,
.bottom-container,
.admin-container {
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

.admin-container {
  border-right: 2px solid rgba(221, 221, 221, 0.87);
  border-left: 2px solid rgba(221, 221, 221, 0.87);
}

.bottom-container,
.top-container,
.admin-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.megaphone,
.chat-icon,
.statistic-icon {
  width: 60px;
}

.bottom-container:hover,
.top-container:hover,
.admin-container:hover {
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

.admin-container.clicked {
  border-right: 5px solid #4f378a;
  border-left: 5px solid #4f378a;
}

.separation-line.posts{
  stroke: rgba(111, 209, 222, 0.85);
}

.separation-line.adminstat{
  stroke: #4f378a;
}

.separation-line.svposts{
  stroke: #2edb7b;
}
</style>
