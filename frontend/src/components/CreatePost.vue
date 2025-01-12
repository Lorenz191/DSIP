<script setup>
import LandingNav from '@/components/LandingNav.vue'
import { onMounted, onUnmounted, ref } from 'vue'
import axios from 'axios'
import router from '@/router/index.js'
import { useToast } from 'vue-toastification'

const postTitle = ref('')
const postContent = ref('')
const loading = ref(false)
const toast = useToast()

const createPost = async () => {
  try {
    loading.value = true
    const response = await axios.post('http://localhost:8000/api/post/create/', {
      title: postTitle.value,
      content: postContent.value
    })
    if (response.status === 201) {
      toast.success('Post wurde erfolgreich erstellt!')
      console.log('Post created successfully:', response.data)
      router.push({ name: 'landing' })
    }
  } catch (error) {
    if (error.response && error.response.status === 400) {
      toast.warning('Dein Post enthält unangebrachte Wörter/Äußerungen, bitte entferne diese!')
      console.log('Error creating post:', error.response.data)
    } else {
      toast.error('Fehler beim Erstellen des Posts!')
      console.log('Error creating post:', error)
    }
  } finally {
    loading.value = false
    postTitle.value = ''
    postContent.value = ''
  }
}

const screenWidth = ref(window.innerWidth)

const updateScreenWidth = () => {
  screenWidth.value = window.innerWidth
}

onMounted(() => {
  window.addEventListener('resize', updateScreenWidth)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateScreenWidth)
})
</script>

<template>
  <LandingNav arrow></LandingNav>
  <div v-if="loading" class="loading-container">
    <span class="loader"> </span>
  </div>
  <div v-else class="content">
    <form @submit.prevent="createPost" :class="[{ 'small-form': screenWidth < 700 }]">
      <div class="header">
        <h1>Neuen Beitrag erstellen</h1>
      </div>
      <input v-model="postTitle" class="titel" type="text" placeholder="Titel" required />
      <textarea
        v-model="postContent"
        class="textarea"
        placeholder="Teile deinen Vorschlag mit uns..."
        required
      ></textarea>
      <div class="buttonDiv">
        <button type="submit" class="create-button">Erstellen</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100vw;
}

form {
  display: flex;
  justify-content: flex-end;
  flex-direction: column;
  width: 50vw;
}

.titel {
  margin-top: 30px;
  border: 1px grey solid;
  border-radius: 10px;
  width: 100%;
  height: 5vh;
}

.header {
  width: 100%;
  margin-top: 50px;
  font-size: 30px;
  font-weight: bolder;
  float: left;
}

.textarea {
  margin-top: 20px;
  border: 1px grey solid;
  border-radius: 10px;
  width: 100%;
  height: 20vh;
  min-height: 25vh;
  max-height: 600px;
  overflow: scroll;
}

.create-button {
  margin-top: 15px;
  background: #d9d9d9;
  font-size: 24px;
  width: 230px;
  height: 40px;
  border-radius: 5px;
  margin-bottom: 60px;
  font-family: Futura;
}

.buttonDiv {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

input {
  text-indent: 10px;
}

textarea {
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

.loader:before,
.loader:after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: #2edb7b;
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
  15%,
  25% {
    transform: translate(-50%, 50%) scale(1);
  }
  50%,
  75% {
    transform: translate(-50%, -30%) scale(0.5);
  }
  80%,
  100% {
    transform: translate(-50%, -50%) scale(0);
  }
}

.small-form {
  display: flex;
  justify-content: flex-end;
  flex-direction: column;
  width: 75vw;
}

.titel {
  margin-top: 30px;
  border: 1px grey solid;
  border-radius: 10px;
  width: 100%;
  height: 5vh;
}

.header {
  width: 100%;
  margin-top: 50px;
  font-size: 30px;
  font-weight: bolder;
  float: left;
}

.textarea {
  margin-top: 30px;
  border: 1px grey solid;
  border-radius: 10px;
  width: 100%;
  height: 20vh;
  min-height: 20vh;
  max-height: 500px;
  overflow: scroll;
}

.create-button {
  margin-top: 15px;
  background: #d9d9d9;
  font-size: 22px;
  width: 230px;
  height: 40px;
  align-self: center;
  border-radius: 5px;
  margin-bottom: 60px;
  font-family: Futura;
}

.buttonDiv {
  float: right;
}

input {
  text-indent: 10px;
}

textarea {
  text-indent: 10px;
}
</style>
