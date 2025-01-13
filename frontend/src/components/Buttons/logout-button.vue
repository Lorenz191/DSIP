<script setup>
import { useAuth0 } from '@auth0/auth0-vue'
import axios from 'axios'

const { logout, getAccessTokenSilently } = useAuth0()

const handleLogOut = async () => {
  try {
    const accessToken = await getAccessTokenSilently()
    const response = await axios.post('http://localhost:8000/api/user/clear/', {
      access_token: accessToken,
    })

    console.log(response)

    if (response.status === 200) {
      logout({
        logoutParams: {
          target: '/'
        }
      })
    }
  } catch (error) {
    console.error('Error during logout:', error)
  }
}

const props = defineProps({
  small: {
    type: Boolean,
    required: false,
    default: false
  }
})
</script>

<template>
  <button v-if="!props.small" class="button__logout" @click="handleLogOut">Abmelden</button>
  <button v-if="props.small" class="button__logout" @click="handleLogOut"><img class="logout-icon"
                                                                               src="../icons/logout-svgrepo-com.svg">
  </button>
</template>

<style scoped>
button {
  color: white;
  font-family: Futura;
  font-weight: bold;
}

.logout-icon {
  width: 30px;
}
</style>
