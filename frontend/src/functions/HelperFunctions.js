import axios from 'axios';

export async function getCSRFToken() {
  try {
    const response = await axios.get("http://localhost:8000/api/csrf/", { withCredentials: true });
    return response.data.csrftoken;
  } catch (error) {
    console.error('Error fetching CSRF token:', error);
    return null;
  }
}
