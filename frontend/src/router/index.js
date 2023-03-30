import Vue from 'vue'
import VueRouter from 'vue-router'
import MetuBotView from '../views/MetuBotView.vue'
import AdminView from '../views/AdminView.vue'
import MetubotAskedQuestions from '../components/MetubotAskedQuestions.vue'
import MetubotQuestionCRUD from '../components/MetubotQuestionCRUD.vue'
import MetubotDashboard from '../components/MetubotDashboard.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'metubot',
    component: MetuBotView,
    meta: { title: 'METUBOT' }
  },
  { // todo: sil
    path: '/deney',
    name: 'metubotDeney',
    component: MetuBotView,
    meta: { title: '??????' },
    props: { enableDidYouMeanThis: true }
  },
  {
    path: '/yonetim',
    name: 'admin',
    children: [

      { path: 'dashboard', component: MetubotDashboard}, //dashboarda soruları koyalım ne dersiniz
      { path: 'tables', component: MetubotAskedQuestions },
      { path: 'charts'},
      { path: 'addquestion', component: MetubotQuestionCRUD },

    ],
    component: AdminView,
    meta: { title: 'METUBOT Yönetim' }
  },
]

const router = new VueRouter({
  routes
})

export default router