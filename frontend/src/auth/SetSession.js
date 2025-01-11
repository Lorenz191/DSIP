import { useAuth0 } from '@auth0/auth0-vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user.js'

export const setSession = async () => {
  const { getAccessTokenSilently, user, logout } = useAuth0()

  try {
    // Get access token and user profile
    const accessToken = await getAccessTokenSilently()

    console.log(user.value)
    console.log(user.value['/roles'])

    // Set session on the backend
    const response = await axios.post(
      'http://localhost:8000/api/set-session/',
      {
        auth0Id: user.value.sub.split('|')[1],
        accessToken: accessToken,
        roles: user.value['/roles'] || []
      },
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`
        },
        withCredentials: true
      }
    )

    console.log('Session successfully set on backend:', response.data)

    const userStore = useUserStore()
    userStore.setUserUuid(user.value.sub)

    return  user.value["/roles"].includes('is_admin')


  } catch (error) {
    console.error('Error during session setup:', error)
    logout({
      logoutParams: {
        target: '/'
      }
    })
  }
}
