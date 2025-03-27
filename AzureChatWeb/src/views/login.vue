<!-- src/views/login.vue -->
<template>
  <div class="container">
    <h2>登录</h2>
    <form @submit.prevent="handleLogin">
      <label for="username">
        <input id="username" type="text" v-model="loginForm.username" placeholder="用户名" required />
      </label>
      <label for="password">
        <input id="password" type="password"
               v-model="loginForm.password" placeholder="密码" required />
      </label>
      <button type="submit" :disabled="loading">登录</button>
    </form>
    <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
    <p>没有账号？<router-link to="/signup">注册</router-link></p>
  </div>
</template>

<script>
import api from '@/utils/api';

export default {
  name: 'LoginView',
  data() {
    return {
      loginForm: {
        username: '',
        password: '',
      },
      errorMessage: '',
      loading: false,
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      try {
        const response = await api.post('/member/login/', this.loginForm);
        const { code, message } = response;
        if (code === 0) {
          const { token, key, user } = response;
          // 保存 token 和 user 信息
          localStorage.setItem('token', token);
          localStorage.setItem('key', key);
          localStorage.setItem('user', JSON.stringify(user));
          this.$router.push('/'); // 假设登录成功后跳转到仪表盘
        } else {
          this.errorMessage = message;
        }
      } catch (error) {
        this.errorMessage = '登录失败，请重试';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
@import "../assets/styles/main.css";
</style>
