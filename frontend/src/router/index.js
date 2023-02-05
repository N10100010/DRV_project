import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Berichte from "@/views/Berichte.vue";
import Rennstrukturanalyse from "@/views/Rennstrukturanalyse.vue";
import AthletenView from "@/views/AthletenView.vue";
import TeamsView from "@/views/TeamsView.vue";
import MedaillenspiegelView from "@/views/MedaillenspiegelView.vue";
import DatenschutzView from "@/views/DatenschutzView.vue";
import ImpressumView from "@/views/ImpressumView.vue";
import HilfeView from "@/views/HilfeView.vue";
import LoginView from "@/views/LoginView.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
            beforeEnter: (to, from, next) => {
                const token = localStorage.getItem('token')
                if (token) {
                    next()
                } else {
                    next({path: '/auth', query: {redirect_to: '/'}})
                }
            }
        },
        {
            path: '/berichte',
            name: 'berichte',
            component: Berichte,
            beforeEnter: (to, from, next) => {
                const token = localStorage.getItem('token')
                if (token) {
                    next()
                } else {
                    next({path: '/auth', query: {redirect_to: '/berichte'}})
                }
            }
        },
        {
            path: '/rennstrukturanalyse/:comp_id?/:event_id?/:race_id?',
            name: 'rennstrukturanalyse',
            component: Rennstrukturanalyse,
            beforeEnter: (to, from, next) => {
                const token = localStorage.getItem('token')
                if (token) {
                    next()
                } else {
                    next({path: '/auth', query: {redirect_to: '/rennstrukturanalyse'}})
                }
            }
        },
        {
            path: '/athleten',
            name: 'athleten',
            component: AthletenView,
            beforeEnter: (to, from, next) => {
                const token = localStorage.getItem('token')
                if (token) {
                    next()
                } else {
                    next({path: '/auth', query: {redirect_to: '/athleten'}})
                }
            }
        },
        {
            path: '/teams',
            name: 'teams',
            component: TeamsView,
            beforeEnter: (to, from, next) => {
                const token = localStorage.getItem('token')
                if (token) {
                    next()
                } else {
                    next({path: '/auth', query: {redirect_to: '/teams'}})
                }
            }
        },
        {
            path: '/medaillenspiegel',
            name: 'medaillenspiegel',
            component: MedaillenspiegelView,
            beforeEnter: (to, from, next) => {
                const token = localStorage.getItem('token')
                if (token) {
                    next()
                } else {
                    next({path: '/auth', query: {redirect_to: '/medaillenspiegel'}})
                }
            }
        },
        {
            path: '/datenschutz',
            name: 'datenschutz',
            component: DatenschutzView,
        },
        {
            path: '/impressum',
            name: 'impressum',
            component: ImpressumView
        },
        {
            path: '/hilfe',
            name: 'hilfe',
            component: HilfeView,
            beforeEnter: (to, from, next) => {
                const token = localStorage.getItem('token')
                if (token) {
                    next()
                } else {
                    next({path: '/auth', query: {redirect_to: '/hilfe'}})
                }
            }
        },
        {
            path: '/auth',
            name: 'Login',
            component: LoginView
        },
    ]
})

export default router
