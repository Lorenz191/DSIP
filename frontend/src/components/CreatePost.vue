<script setup>

import LandingNav from "@/components/LandingNav.vue";
import {ref} from "vue";
import axios from "axios";
import router from "@/router/index.js";
const postTitle = ref('')
const postContent = ref('')
const loading = ref(false)
const createPost = async() => {
  try {
    loading.value = true;
    await axios.post('http://localhost:8000/api/post/create/', {
      body: {
        title: postTitle.value,
        content: postContent.value
      }
    })
  } catch (error) {
    console.error('Error creating post:', error)
  } finally {
    postTitle.value = '';
    postContent.value = '';
    router.push({name: 'landing'})
  }
}

</script>

<template>
  <LandingNav :arrow="true" :searchbar="false"></LandingNav>
  <div v-if="loading" class="loading-container">
      <span class="loader"> </span>
  </div>
  <div v-else class="content">
    <form @submit.prevent="createPost">
      <div class="header">
        <h1>Neuen Beitrag erstellen</h1>
      </div>
    <input v-model="postTitle" class="titel" type="text" placeholder="Titel" required>
      <textarea v-model="postContent" class="textarea" placeholder="Teile deinen Vorschlag mit uns..." required></textarea>
      <div class="buttonDiv">
        <button type="submit" class="create-button">
            Erstellen
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
  .content{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100vw;
  }
form{
  width: 40vw;
  display: flex;
  justify-content: flex-end;
  flex-direction: column;
}
  .titel{
    margin-top: 30px;
    border: 1px grey solid;
    border-radius: 10px;
    width: 100%;
    height: 5vh;
  }
h1{
  float: left;
}
  .header{
    width: 100%;
    margin-top: 50px;
    font-size: 30px;
    font-weight: bolder;
    float: left;
  }
  .textarea{
    margin-top: 30px;
    border: 1px grey solid;
    border-radius: 10px;
    width: 100%;
    height: 20vh;
    min-height: 20vh;
    max-height: 500px;
    overflow: scroll;
  }
  .create-button{
    float: right;
    margin-top: 15px;
    background: #D9D9D9;
    font-size: 24px;
    width: 230px;
    height: 40px;
    border-radius: 5px;
    margin-bottom: 60px;
    font-family: Futura;
  }
  .buttonDiv{
    float: right;
  }
  input{
  text-indent: 10px;
  }
  textarea{
  text-indent: 10px;
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
</style>
