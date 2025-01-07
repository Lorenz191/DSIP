import { createRouter, createWebHistory } from 'vue-router';
import LogInView from "../views/LogInView.vue";
import LandingPageView from '@/views/LandingPageView.vue'
import PostView from '@/views/PostView.vue'
import CreatePost from "@/components/CreatePost.vue";
import CallbackPage from '@/views/callback-page.vue'
import ProfileView from "@/views/ProfileView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LogInView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/LogInView.vue')
    },
    {path: '/landing', name: 'landing', component: LandingPageView},
    {path: '/post/:id', name: 'post', component: PostView},
    {path: "/create", name:'create', component: CreatePost},
    {path: "/callback", name: 'callback', component: CallbackPage},
    {path: '/profile', name:'profile', component: ProfileView},
  ]
})

export default router
