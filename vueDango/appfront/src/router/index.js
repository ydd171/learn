import Vue from 'vue'
import Router from 'vue-router'
import execl from '@/components/execl'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'execl',
      component: execl
    }
  ]
})
