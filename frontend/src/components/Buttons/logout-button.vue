<script setup>
import { useAuth0 } from '@auth0/auth0-vue'

const { logout } = useAuth0()

const handleLogOut = () => {
  logout({
    logoutParams: {
      target: '/'
    }
  })
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
  <button v-if="props.small" class="button__logout" @click="handleLogOut"><img class="logout-icon" src="../icons/logout-svgrepo-com.svg"></button>
</template>

<style scoped>
button {
  color: white;
  font-family: Futura;
  font-weight: bold;
}
.logout-icon{
  width: 30px;
}

</style>
