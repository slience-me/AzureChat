// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '@/views/login.vue';
import SignupView from '@/views/signup.vue';
import ChatViews from '@/views/chat.vue'; // 假设有一个聊天页面
// 定义路由
const routes = [
  {
    path: '/',
    redirect: '/chat', // 访问首页自动跳转到 /chat
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupView,
  },
  {
    path: '/chat',
    name: 'chat',
    component: ChatViews,
    meta: { requiresAuth: true }, // 需要认证才能访问
  },
];

// 创建路由实例
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// 路由守卫，检查是否需要认证
router.beforeEach((to, from, next) => {
  // 如果目标路由需要认证（meta.requiresAuth）
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    const token = localStorage.getItem('token');
    if (!token) {
      // 如果没有 token，跳转到登录页
      next('/login');
    } else {
      next(); // 如果有 token，允许访问
    }
  } else {
    next(); // 不需要认证的路由直接跳转
  }
});

export default router;
