import auth0 from 'auth0-js'
import EventEmitter from 'eventemitter3'
import router from './../router'
import axios from 'axios'
import { useUserStore } from './../stores/user.js'


export default class AuthService {
  authenticated = this.isAuthenticated()
  authNotifier = new EventEmitter()

  constructor() {
    this.login = this.login.bind(this)
    this.setSession = this.setSession.bind(this)
    this.logout = this.logout.bind(this)
    this.isAuthenticated = this.isAuthenticated.bind(this)
    this.handleAuthentication = this.handleAuthentication.bind(this)
  }


  // create an instance of auth0.WebAuth with your
  // API and Client credentials
  auth0 = new auth0.WebAuth({
    domain: import.meta.env.VITE_AUTH0_DOMAIN,
    clientID: import.meta.env.VITE_AUTH0_CLIENT_ID,
    redirectUri: 'http://localhost:8080',
    audience: 'https://dsip.at/login',
    responseType: 'token id_token',
    scope: 'openid profile'
  })

  // this method calls the authorize() method
  // which triggers the Auth0 login page
  login() {
    console.log('Login method called');
    this.auth0.authorize((err) => {
      if (err) {
        console.error('Error during login:', err);
      }
    });
  }

  // this method calls the parseHash() method of Auth0
  // to get authentication information from the callback URL
  handleAuthentication() {
    this.auth0.parseHash((err, authResult) => {
      if (authResult && authResult.accessToken && authResult.idToken) {
        this.setSession(authResult)
      } else if (err) {
        console.log(err)
      } else {
        this.silentAuth()
          .then(() => {
            console.log('user logged in through silent auth')
          })
          .catch((err) => {
            console.log(err)
          })
      }
      router.replace('/')
    })
  }

  // stores the user's access_token, id_token, and a time at
  // which the access_token will expire in the local storage
  setSession(authResult) {
    this.accessToken = authResult.accessToken
    this.idToken = authResult.idToken
    this.profile = authResult.idTokenPayload
    this.expiresAt = authResult.expiresIn * 1000 + new Date().getTime()
    this.authNotifier.emit('authChange', { authenticated: true })

    axios.post('http://localhost:8000/api/set-session/', {
      auth0Id: this.profile.sub.split('|')[1]
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.accessToken}`
      }
    })
    .then(response => {
      console.log('Session set on backend:', response.data)
      router.push({name: 'landing'})
      useUserStore().setUserUuid(this.profile.sub.split('|')[1])
    })
    .catch(error => {
      console.error('Error setting session on backend:', error)
    })
  }

  // remove the access and ID tokens from the
  // local storage and emits the authChange event
  logout() {
    delete this.accessToken
    delete this.idToken
    delete this.expiresAt
    this.authNotifier.emit('authChange', false)
    useUserStore().clearUserUuid()
    // navigate to the home route
    router.replace('/')
  }

  // checks if the user is authenticated
  isAuthenticated() {
    // Check whether the current time is past the
    // access token's expiry time
    return new Date().getTime() < this.expiresAt
  }

  // a static method to get the access token
  getAuthToken() {
    return this.accessToken
  }

  // a method to get the User profile
  getUserProfile() {
    return this.profile
  }

  silentAuth() {
    return new Promise((resolve, reject) => {
      this.auth0.checkSession({}, (err, authResult) => {
        if (err) return reject(err)
        this.setSession(authResult)
        resolve()
      })
    })
  }
}
