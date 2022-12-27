import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MenView from '../views/MenView.vue'
import WomenView from '../views/WomenView.vue'
import SonstigesView from "@/views/SonstigesView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/women',
      name: 'women',
      component: () => WomenView
    },
    {
      path: '/men',
      name: 'men',
      component: () => MenView
    },
    {
      path: '/sonstiges',
      name: 'sonstiges',
      component: () => SonstigesView
    }
  ]
})

export default router
