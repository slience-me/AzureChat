import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/', // Django 后端的 URL
  timeout: 5000, // 请求超时时间
});

// 请求拦截器：添加 token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      // eslint-disable-next-line no-param-reassign
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// 响应拦截器：处理错误信息
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // 处理认证失败（例如 token 过期）
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  },
);

// 封装 GET 请求
const get = (url, params = {}) => api.get(url, { params })
  .then((response) => response.data)
  .catch((error) => {
    console.error('GET请求失败:', error);
    throw error; // 抛出错误，调用者可以处理
  });

// 封装 POST 请求
const post = (url, data = {}) => api.post(url, data)
  .then((response) => response.data)
  .catch((error) => {
    console.error('POST请求失败:', error);
    throw error; // 抛出错误，调用者可以处理
  });

// 其他封装的请求方法可以继续按需添加...

export default {
  get,
  post,
};
