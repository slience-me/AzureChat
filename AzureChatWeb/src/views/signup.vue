<!-- src/views/Signup.vue -->
<template>
  <div class="container">
    <h2>注册</h2>
    <form @submit.prevent="handleSignup">
      <label for="username">用户名:
        <input id="username" type="text" v-model="signup.username" placeholder="用户名" required />
      </label>
      <label for="password">密码:
        <input id="password" type="password" v-model="signup.password" placeholder="密码" required />
      </label>
      <button type="submit" :disabled="loading">注册</button>
    </form>
    <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
    <p>已有账号？<router-link to="/login">登录</router-link></p>
  </div>
</template>

<script>
import api from '@/utils/api';

export default {
  name: 'SignupView',
  data() {
    return {
      signup: {
        username: '',
        password: '',
      },
      errorMessage: '',
      loading: false,
    };
  },
  methods: {
    async handleSignup() {
      this.loading = true;
      try {
        const response = await api.post('/member/signup/', this.signup);
        const { code, msg } = response;
        if (code === 0) {
          alert(`${msg}跳转到登录页`);
          this.$router.push('/login'); // 注册成功后跳转到登录页
        } else {
          this.errorMessage = msg;
        }
      } catch (error) {
        this.errorMessage = '注册失败，请重试';
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
