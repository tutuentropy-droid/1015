import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
    meta: { title: '首页 - 志愿填报' },
  },
  {
    path: '/colleges',
    name: 'Colleges',
    component: () => import('../views/CollegesView.vue'),
    meta: { title: '院校查询' },
  },
  {
    path: '/colleges/:id',
    name: 'CollegeDetail',
    component: () => import('../views/CollegeDetailView.vue'),
    meta: { title: '院校详情' },
  },
  {
    path: '/plan',
    name: 'Plan',
    component: () => import('../views/PlanView.vue'),
    meta: { title: '志愿方案' },
  },
  {
    path: '/compare',
    name: 'CollegeCompare',
    component: () => import('../views/CollegeCompareView.vue'),
    meta: { title: '院校对比' },
  },
  {
    path: '/subject-analysis',
    name: 'SubjectAnalysis',
    component: () => import('../views/SubjectAnalysisView.vue'),
    meta: { title: '选科影响分析' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || '高考志愿填报决策系统'
  next()
})

export default router
