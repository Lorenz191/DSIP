import { useAuth0 } from '@auth0/auth0-vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user.js';

export const setSession = async () => {
  const { getAccessTokenSilently, user, logout } = useAuth0();

  try {
    const accessToken = await getAccessTokenSilently();
    const profile = user.value;

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
          Authorization: `Bearer ${accessToken}`,
        },
        withCredentials: true,
      }
    );

    console.log('Session successfully set on backend:', response.data);

    const userStore = useUserStore();
    userStore.setUserUuid(response.data.uuid);
  } catch (error) {
    console.error('Error during session setup:', error);
    logout({
        logoutParams: {
          target: '/'
        }
      })
  }
};
