<script setup>
import {ref, onMounted, onUnmounted} from 'vue'

import LoginButton from '@/components/Buttons/login-button.vue'
import EasySponsor from "@/components/easySponsor.vue";

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


</script>

<template>
  <div class="all">
  <div :class="[{'container' : screenWidth>=850}, {'container-small': screenWidth<850}]">
    <div class="left-section">
      <img v-if="screenWidth>=850" src="../components/icons/Title_Picture.svg" alt="Picture" class="title-image" />
      <img v-else style="scale: 120%" src="../components/icons/Parliament_Small.svg" alt="Picture" class="title-image"/>
    </div>

    <div class="right-section">
      <div class="text-container">
        <h1>Digitales Schülerparlament</h1>
      </div>
      <div class="login-container">
        <LoginButton></LoginButton>
      </div>
    </div>
     <div v-if="screenWidth<850" class="left-section">
      <img src="../components/icons/Parliament_Small.svg" alt="Picture" class="title-image smallUnder"/>
    </div>
  </div>
  </div>
  <easy-sponsor></easy-sponsor>
</template>

<style scoped>
*{
  font-family: Futura,sans-serif;
}
.container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  height: 90vh;
  width: 90vw;
}

.left-section {
  flex: 1.5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.title-image {
  max-height: 100%;
  max-width: 90%;
  object-fit: contain;
}


.right-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  border-radius: 10px;
  filter: drop-shadow(4px 4px 0.75rem #AAAAAA);
  background-color: white;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

.login-button {
  background-color: #6ee7b7;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.login-button a {
  color: inherit;
  text-decoration: none;
}

.login-button:hover {
  background-color: #34d399;
}
.all{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 93vh;
  width: 100vw;
}

.text-container{
  display: flex;
  justify-content: center;
  align-items: flex-start;
  margin-top: 1rem;
  text-align: center;
}
h1{
  font-weight: bold;
  font-size: large;
}
.container-small{
  width: 85vw;
  .text-container{
    width: 90%;
  }
}
.smallUnder{
  z-index: -1;
  rotate: 180deg;
  scale: 120%;
}
</style>
