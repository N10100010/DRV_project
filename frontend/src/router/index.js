import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Berichte from "@/views/Berichte.vue";
import Wettkampfresultate from "@/views/WettkampfresultateView.vue";
import Rennstrukturanalyse from "@/views/Rennstrukturanalyse.vue";
import AthletenView from "@/views/AthletenView.vue";
import TeamsView from "@/views/TeamsView.vue";
import MedallienspiegelView from "@/views/MedallienspiegelView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => HomeView
    },
    {
      path: '/berichte',
      name: 'berichte',
      component: () => Berichte
    },
    {
      path: '/wettkampfresultate',
      name: 'wettkampfresultate',
      component: () => Wettkampfresultate
    },
    {
      path: '/rennstrukturanalyse',
      name: 'rennstrukturanalyse',
      component: () => Rennstrukturanalyse
    },
    {
      path: '/athleten',
      name: 'athleten',
      component: () => AthletenView
    },
    {
      path: '/teams',
      name: 'teams',
      component: () => TeamsView
    },
    {
      path: '/medallienspiegel',
      name: 'medallienspiegel',
      component: () => MedallienspiegelView
    }
  ]
})

export default router
