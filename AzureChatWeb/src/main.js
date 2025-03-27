import { createApp } from 'vue'; // 从 vue 导入 createApp
import App from './App.vue'; // 导入根组件 App.vue
import router from './router'; // 导入 Vue Router 配置
// import store from './store'; // 导入 Vuex 配置（如果使用）

const app = createApp(App); // 使用 createApp 创建应用实例

// 配置 Vue Router 和 Vuex
app.use(router); // 注册路由
// app.use(store); // 注册 Vuex 状态管理

// 挂载到 #app 元素
app.mount('#app'); // 挂载到 id 为 app 的 DOM 元素
