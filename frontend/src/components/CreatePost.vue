<script setup>

import LandingNav from "@/components/LandingNav.vue";
import {ref} from "vue";
import axios from "axios";
const postTitle = ref('')
const postContent = ref('')

const createPost = async() => {
  try {
    await axios.post('http://localhost:8080/api/posts/create', {
      body: {
        title: postTitle.value,
        content: postContent.value
      }
    })

  } catch (error) {
    console.error('Error creating post:', error)
  }
}

</script>

<template>
  <LandingNav :arrow="true" :searchbar="false"></LandingNav>

  <div class="content">
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
</style>
