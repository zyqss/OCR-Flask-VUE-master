
import Vue from 'vue'
import Router from 'vue-router'
import Menu from '../views/Menu.vue'
import Login from '../views/Login.vue'
import IdentityCard from '../views/IdentityCard.vue'
import Fapiao from '../views/Fapiao.vue'
import Ticket from '../views/Ticket.vue'
import BusinessLicense from '../views/BusinessLicense.vue'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/menu', // path 设置为 “/” ，默认显示该页面
      component: Menu,
      name: 'Menu'
    },
    {
      path: '/',
      component: Login,
      name: 'login'
    },
    {
      path: '/identitycard',
      component: IdentityCard,
      name: 'IdentityCard'
    },
    {
      path: '/fapiao',
      component: Fapiao,
      name: 'Fapiao'
    },
    {
      path: '/ticket',
      component: Ticket,
      name: 'Ticket'
    },
    {
      path: '/businesslicense',
      component: BusinessLicense,
      name: 'Business'
    },

  ],
  mode: 'history' // mode 设置为history ，去掉地址栏上的 # 号
})
