import Vue from 'vue'
import VueRouter from 'vue-router'
import MetuBotView from '../views/MetuBotView.vue'
import AdminView from '../views/AdminView.vue'
import AdminAskedQuestions from '../components/AdminAskedQuestions.vue'
import MetubotQuestionCRUD from '../components/AdminQuestionCRUD.vue'
import MetubotDashboard from '../components/AdminDashboard.vue'
import AdminChart from '@/components/AdminChart.vue';
import AdminLogin from '@/components/AdminLogin.vue';

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
      { path: 'tables', component: AdminAskedQuestions },
      { path: 'charts', component: AdminChart},
      { path: 'addquestion', component: MetubotQuestionCRUD },

    ],
    component: AdminView,
    meta: { title: 'METUBOT Yönetim' }
  },
  {
    path: '/login',
    name: 'login',
    component: AdminLogin,
    meta: { title: 'METUBOT Yönetim Login' }
  },
]

const router = new VueRouter({
  routes
})

export default router
