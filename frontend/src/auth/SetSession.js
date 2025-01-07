import { useAuth0 } from '@auth0/auth0-vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user.js'

export const setSession = async () => {
  const { getAccessTokenSilently, user, logout } = useAuth0()

  try {
    // Get access token and user profile
    const accessToken = await getAccessTokenSilently()
    const profile = user.value

    // Set session on the backend
    const response = await axios.post(
      'http://localhost:8000/api/set-session/',
      {
        auth0Id: profile.sub.split('|')[1],
        accessToken: accessToken,
        roles: profile['/roles'] || []
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

    // Only proceed to get user data if session was set successfully
    const userStore = useUserStore()
    userStore.setUserUuid(response.data.uuid)

    const userResponse = await axios.get('http://localhost:8000/api/user/get/')
    console.log(userResponse.data)

    return  userResponse.data.roles.includes('is_admin')


  } catch (error) {
    console.error('Error during session setup:', error)
    logout({
      logoutParams: {
        target: '/'
      }
    })
  }
}
