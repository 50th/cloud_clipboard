import { createRouter, createWebHistory, type RouteRecordName } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { checkAccessApi } from '@/apis/userApis'

const NeedLoginRoutes: RouteRecordName[] = [
  'editArticle',
  'addArticle',
  'tool',
  'videoList',
  'playVideo',
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('@/views/AboutView.vue'),
    },
    {
      path: '/add-clipboards',
      name: 'addClipboard',
      component: () => import('@/views/ClipboardViews/AddClipboard.vue'),
    },
    {
      path: '/clipboards',
      name: 'clipboardList',
      component: () => import('@/views/ClipboardViews/ClipboardList.vue'),
    },
    {
      path: '/clipboards/:id',
      name: 'clipboardIndex',
      component: () => import('@/views/ClipboardViews/ClipboardIndex.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
  ],
})

router.beforeEach(async (to, from) => {
  let user = useUserStore().getUser()
  if (user) {
    await checkAccessApi(user.access)
      .then((res) => {
        if (res.code === 1003 || res.code === 1005) {
          useUserStore().setUser(null)
          user = null
        }
      })
      .catch((err) => {
        useUserStore().setUser(null)
        user = null
      })
  }

  if (to.name === 'login' && user) {
    return { name: 'home' }
  }

  if (!user && to.name && NeedLoginRoutes.includes(to.name as RouteRecordName)) {
    return { name: 'home' }
  }
})

export default router
