<script setup>
import { ref, onMounted } from 'vue'

const easynameUrl = ref('https://www.easyname.at/de/unternehmen/presse\n')
import AuthService from '../auth/AuthService'
const auth = new AuthService()


const authenticated = ref(false)
const message = ref('')
const userProfile = ref(null)

const handleAuthentication = () => {
  auth.handleAuthentication()
}

const login = () => {
  auth.login()
}



onMounted(() => {
  handleAuthentication()

  auth.authNotifier.on('authChange', (authState) => {
    authenticated.value = authState.authenticated
    if (authState.authenticated) {
      userProfile.value = auth.getUserProfile()
    } else {
      userProfile.value = null
      message.value = ''
    }
  })
})


</script>

<template>
  <div class="all">
  <div class="container">
    <div class="left-section">
      <img src="../components/icons/Title_Picture.svg" alt="Picture" class="title-image" />
    </div>

    <div class="right-section">
      <div class="text-container">
        <h1>Digitales Schülerparlament</h1>
      </div>
      <div class="login-container">
        <button class="btn btn-primary btn-margin login-button" v-if="!authenticated" @click="login" type="submit">
          Anmelden
        </button>
      </div>
    </div>
  </div>
  </div>
  <div class="sponsor">
    <p>Powered by <a :href="easynameUrl" target="_blank"><img src="https://static.easyname.com/images/svg/singles/logos/easyname/easyname_logo_default.svg?v=2" height="40" alt=""></a></p>
  </div>
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
.sponsor {
  display: flex;
  justify-content: center;
  flex-direction: row;
}
</style>
