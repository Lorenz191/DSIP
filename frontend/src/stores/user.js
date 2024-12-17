import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const userUuid = ref(localStorage.getItem('userUuid'))
  const accessToken = ref(localStorage.getItem('accessToken'))

  function setUserUuid(uuid) {
    userUuid.value = uuid
    localStorage.setItem('userUuid', uuid)
  }

  function clearUserUuid() {
    userUuid.value = null
    localStorage.removeItem('userUuid')
  }

  return { userUuid, setUserUuid, clearUserUuid }
})
