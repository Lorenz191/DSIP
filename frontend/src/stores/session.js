import { defineStore } from 'pinia'

export const useSessionStore = defineStore('session', {
  state: () => ({
    isSessionSet: false,
    isAdmin: false
  }),
  actions: {
    setSessionStatus(isSet, isAdmin) {
      this.isSessionSet = isSet
      this.isAdmin = isAdmin
    }
  }
})
