import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Berichte from "@/views/Berichte.vue";
import Wettkampfresultate from "@/views/WettkampfresultateView.vue";
import Rennstrukturanalyse from "@/views/Rennstrukturanalyse.vue";
import AthletenView from "@/views/AthletenView.vue";
import TeamsView from "@/views/TeamsView.vue";
import MedaillenspiegelView from "@/views/MedaillenspiegelView.vue";
import DatenschutzView from "@/views/DatenschutzView.vue";
import ImpressumView from "@/views/ImpressumView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/berichte',
      name: 'berichte',
      component: Berichte
    },
    {
      path: '/wettkampfresultate',
      name: 'wettkampfresultate',
      component: Wettkampfresultate
    },
    {
      path: '/rennstrukturanalyse',
      name: 'rennstrukturanalyse',
      component: Rennstrukturanalyse
    },
    {
      path: '/athleten',
      name: 'athleten',
      component: AthletenView
    },
    {
      path: '/teams',
      name: 'teams',
      component: TeamsView
    },
    {
      path: '/medaillenspiegel',
      name: 'medaillenspiegel',
      component: MedaillenspiegelView
    },
      {
      path: '/datenschutz',
      name: 'datenschutz',
      component: DatenschutzView
    },
      {
      path: '/impressum',
      name: 'impressum',
      component: ImpressumView
    }
  ]
})

export default router
