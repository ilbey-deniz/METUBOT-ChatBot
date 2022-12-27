import Vue from 'vue'
import VueRouter from 'vue-router'
import MetuBotView from '../views/MetuBotView.vue'
import AdminView from '../views/AdminView.vue'
import MetubotAskedQuestions from '../components/MetubotAskedQuestions.vue'
import MetubotAddQuestion from '../components/MetubotAddQuestion.vue'

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
    children: [

      { path: 'dashboard'},
      { path: 'tables', component: MetubotAskedQuestions },
      { path: 'charts'},
      { path: 'addquestion', component: MetubotAddQuestion },

    ],
    component: AdminView,
    meta: { title: 'METUBOT Yönetim' }
  },
]

const router = new VueRouter({
  routes
})

export default router
