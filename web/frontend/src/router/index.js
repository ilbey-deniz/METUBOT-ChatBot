import Vue from 'vue'
import VueRouter from 'vue-router'
import MetuBotView from '../views/MetuBotView.vue'
import AdminView from '../views/AdminView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'metubot',
    component: MetuBotView,
    meta: { title: 'METUBOT' }
  },
  {
    path: '/yonetim',
    name: 'admin',
    component: AdminView,
    meta: { title: 'METUBOT Yönetim' }
  }
]

const router = new VueRouter({
  routes
})

export default router
