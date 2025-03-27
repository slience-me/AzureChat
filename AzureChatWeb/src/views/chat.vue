<template>
  <div class="layout">
    <!-- 左侧历史会话 -->
    <div class="sidebar">
      <button class="new-conversation-btn" @click="createNewConversation">开启新会话</button>
      <ul>
        <li v-for="conversation in conversations" :key="conversation.id"
            @keydown.enter="selectConversation(conversation.id)"
            @keydown.space="selectConversation(conversation.id)"
            tabindex="0"
            @click="selectConversation(conversation.id)"
            class="conversation-item-wrapper"
            @mouseover="conversation.showDelete = true"
            @focusin="conversation.showDelete = true"
            @mouseleave="conversation.showDelete = false"
            @focusout="conversation.showDelete = false">
          <div class="conversation-item">
            <span class="conversation-title">{{ conversation.summary }}</span>
<!--            <span class="conversation-last-message">
          {{ conversation.summary }}
        </span>-->
<!--             显示 × 按钮-->
            <span v-if="conversation.showDelete"
                  class="delete-btn"
                  @keydown.enter="deleteConversation(conversation.id)"
                  @keydown.space="deleteConversation(conversation.id)"
                  @click.stop="deleteConversation(conversation.id)">
              ×
            </span>
          </div>
        </li>
      </ul>
    </div>

    <!-- 右侧内容区域 -->
    <div class="main">
      <!-- 导航栏 -->
      <header class="navbar">
        <div class="user-info">
          <img src="/avator.jpg" alt="头像" class="avatar" />
          <span class="username">{{ username }}</span>
          <button @click="logout" class="logout-btn">退出登录</button>
        </div>
      </header>

      <!-- 当前聊天区 -->
<!--      <div class="chat-box">-->
<!--        <div class="chat-history">-->
<!--          <div v-for="(message, index) in currentConversation.messages"-->
<!--               :key="index" class="message">-->
<!--            <span class="message-user">{{ message.user }}:</span> {{ message.content }}-->
<!--          </div>-->
<!--        </div>-->
<!--        <div class="chat-input">-->
<!--          <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="输入你的消息..." />-->
<!--        </div>-->
<!--      </div>-->

      <div class="chat-bot-area">
        <section class="content" ref="msgContainer">
          <ul id="chat-area" v-for="(message, index) in chatMessages" :key="index">
            <li v-if="message.sender == 'assistant'">
              <div class="balloon">
                <img class="img-circle" src="openai.png" alt="image" />
                <p class="talk" v-html="convertMarkdown(message.message)"></p>
<!--                <p class="talk">{{ message.message }}</p>-->
              </div>
            </li>
            <li v-else>
              <div class="balloon balloon-r">
<!--                <p class="talk talk-r">{{ message.message }}</p>-->
                <p class="talk talk-r" v-html="convertMarkdown(message.message)"></p>
              </div>
            </li>
          </ul>
        </section>
        <footer class="footer">
          <input
              id="msg-send"
              class="msg-input"
              placeholder="请输入消息"
              v-model="prompt"
              v-on:keyup.enter="sendMessage()"
          />
          <button class="btn-submit" type="button" @click="sendMessage()">发送
          </button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script>
import { Toast } from '@/utils/helpers';
import api from '@/utils/api';
import { marked } from 'marked'; // 导入 marked 库
import DOMPurify from 'dompurify';

export default {
  name: 'ChatViews',
  data() {
    return {
      currentConversationId: '',
      username: '小明', // 当前用户名字
      conversations: [{ id: 1, member__username: 'slience_me', summary: 'eat dinner' }],
      newMessage: '',
      prompt: '',
      chatMessages: [],
    };
  },
  watch: {
    chatMessages: {
      handler() {
        window.scrollTo({
          left: 0,
          top: document.body.scrollHeight,
          behavior: 'smooth',
        });
      },
      deep: true,
    },
  },
  mounted() {
    this.getAllConversations();
    // this.getAllChatRecord(this.conversations[0].id);
    // this.currentConversationId = this.conversations[0].id;
  },
  methods: {
    convertMarkdown(message) {
      // 转换 Markdown 到 HTML 并清理不安全的 HTML
      const htmlContent = marked(message);
      return DOMPurify.sanitize(htmlContent);
    },
    async deleteConversation(id) {
      try {
        const response = await api.get(`/message/conversations/${id}/del`);

        if (response.code === 0) {
          // 删除成功，更新本地会话列表
          this.conversations = this.conversations.filter((conversation) => conversation.id !== id);
          Toast.fire({
            icon: 'success',
            title: '会话已删除',
          });
        } else {
          Toast.fire({
            icon: 'error',
            title: '删除失败，请重试！',
          });
        }
      } catch (error) {
        Toast.fire({
          icon: 'error',
          title: '请求失败，请重试！',
        });
      }
    },
    // 切换显示/隐藏删除菜单
    toggleMenu(index) {
      // 先关闭所有菜单，然后再打开当前项的菜单
      this.conversations.forEach((conversation, i) => {
        if (i !== index) {
          // eslint-disable-next-line no-param-reassign
          conversation.showMenu = false;
        }
      });

      // 切换当前会话的菜单显示状态
      this.conversations[index].showMenu = !this.conversations[index].showMenu;
    },
    async createNewConversation() {
      try {
        const response = await api.post('/message/conversations/new');
        // await this.getAllConversations();
        console.log(response);
        console.log(response.data);
        this.selectConversation(response.data.id);
      } catch (error) {
        Toast.fire({
          icon: 'error',
          title: '请求失败,请重试！',
        });
      }
    },
    selectConversation(id) {
      this.currentConversationId = id;
      this.getAllChatRecord(id); // 获取聊天记录
    },
    async getAllConversations() {
      try {
        const response = await api.get('/message/conversations/');
        console.log(response);
        this.conversations = response.data;
      } catch (error) {
        Toast.fire({
          icon: 'error',
          title: '请求失败,请重试！',
        });
      }
    },
    async getAllChatRecord(id) {
      try {
        const response = await api.get(`/message/conversations/${id}/chat_records/`);
        console.log(response);
        this.chatMessages = response.data;
        if (response.data.length === 0) {
          this.chatMessages.push({
            message: '您好，我是 Azure OpenAI 的 ChatGPT，有任何问题都可以问我 ^_^',
            sender: 'assistant',
          });
        }
      } catch (error) {
        Toast.fire({
          icon: 'error',
          title: '请求失败,请重试！',
        });
      }
    },
    sendMessage() {
      if (this.prompt !== '') {
        this.showUserMessage();
        this.getBotMessage(this.prompt);
        this.prompt = '';
      } else {
        Toast.fire({
          icon: 'error',
          title: '请输入消息 !',
        });
      }
    },
    showUserMessage() {
      this.chatMessages.push({
        message: this.prompt,
        sender: 'user',
      });
    },
    async getBotMessage(prompt) {
      try {
        const conversationId = this.currentConversationId;
        const response = await api.post('/message/chat/', { prompt, conversationId });
        const botMessage = response.message;
        this.chatMessages.push({
          message: botMessage,
          sender: 'assistant',
        });
      } catch (error) {
        Toast.fire({
          icon: 'error',
          title: 'AI 请求失败',
        });
      }
    },
    async logout() {
      try {
        const key = localStorage.getItem('key');
        const res = await api.post('/member/logout/', { key });
        if (res.code === 1) {
          console.log(res.message);
        } else {
          localStorage.clear();
          this.$router.push('/login');
        }
      } catch (error) {
        Toast.fire({
          icon: 'error',
          title: '请求失败，请重试!',
        });
      }
    },
  },
};
</script>

<style scoped>
/* Add global styles for layout and sidebar */
.layout {
  display: flex;
  height: 100vh;
  font-family: 'Arial', sans-serif;
  background-color: #f4f6f9;
  overflow: hidden; /* 防止溢出 */
}

.sidebar {
  width: 280px;
  background-color: #ffffff;
  color: #2c3e50;
  padding: 20px;
  box-sizing: border-box;
  border-right: 1px solid #ddd;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  height: 100%; /* 确保左侧栏占满父容器高度 */
  overflow-y: auto; /* 如果内容超出高度，则出现滚动条 */
}

.main {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 防止超出右侧区域溢出 */
  padding-bottom: 70px; /* 为底部输入框区域留出空间 */
}

.chat-bot-area {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  padding: 20px;
  padding-bottom: 100px; /* 留出更多空间给底部 */
  height: calc(100vh - 70px); /* 动态计算聊天区域的高度，减去输入框的高度 */
}

.sidebar ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.sidebar li {
  margin-bottom: 15px;
}

.conversation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
}

.conversation-item:hover {
  background-color: #f0f0f0;
}

.conversation-title {
  font-size: 16px;
  font-weight: bold;
}

.conversation-last-message {
  font-size: 14px;
  color: #bdc3c7;
}

.navbar {
  display: flex;
  justify-content: flex-end; /* 让内容右对齐 */
  align-items: center;
  padding: 10px 20px;
  background-color: #ffffff;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1); /* 添加阴影，使 navbar 更加立体 */
}

.user-info {
  display: flex;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 20px; /* 头像和用户名之间的间距 */
}

.username {
  margin-right: 15px; /* 用户名和按钮之间的间距 */
  font-size: 16px;
  color: #333;
  width: 100px;
}

.logout-btn {
  padding: 5px 15px;
  border: none;
  background-color: #ff4d4f; /* 红色背景 */
  color: white;
  font-size: 14px;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-btn:hover {
  background-color: #ff3333; /* 悬停时的背景色变化 */
}

.chat-box {
  flex-grow: 1;
  padding: 20px;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  border-top: 1px solid #f0f0f0;
}

.chat-history {
  flex-grow: 1;
  overflow-y: auto;
  margin-bottom: 15px;
}

.message {
  background-color: #ecf0f1;
  padding: 12px;
  border-radius: 10px;
  margin-bottom: 10px;
}

.chat-input {
  display: flex;
  justify-content: space-between;
}

.chat-input input {
  width: 90%;
  padding: 12px;
  font-size: 16px;
  border-radius: 20px;
  border: 1px solid #ccc;
}

/* Chatbot specific styles */
.header {
  top: 0;
  position: sticky;
  z-index: 1;
  width: 100%;
  height: 50px;
  font-size: 18px;
  text-align: center;
  line-height: 50px;
  background-color: rgb(30, 144, 255);
  color: white;
}

.content {
  width: 100%;
  min-height: 300px;
  margin-bottom: 50px;
  background-color: #f5f5f5;
}

#chat-area {
  padding: 10px;
  list-style: none;
}

.balloon {
  margin: 20px 0;
  display: flex;
  align-items: center;
}

.balloon-r {
  margin-right: 15px;
  justify-content: flex-end;
  align-items: center;
}

.img-circle {
  width: 40px;
  height: 40px;
  margin: 0 15px;
  border-radius: 25px;
  background-color: white;
}

.talk {
  max-width: 500px;
  padding: 10px;
  border-radius: 10px;
  background-color: #ffffff;
}

.talk-r {
  background-color: #95ec69;
}

button {
  /* width: 33%; */
  padding: 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.footer {
  position: fixed;
  bottom: 0;
  width: 100%;
  height: 70px;
  display: flex;
  align-items: center;
  background-color: #ffffff;
  box-shadow: 0px -2px 10px rgba(0, 0, 0, 0.1); /* 为底部添加阴影效果 */
  padding: 10px 20px;
  box-sizing: border-box;
  z-index: 1; /* 确保输入框在其他内容之上 */
}

.msg-input {
  width: 70%;
  padding: 12px 20px;
  border: 1px solid #ddd;
  border-radius: 30px;
  font-size: 16px;
  outline: none;
  transition: all 0.3s ease;
  background-color: #f7f7f7; /* 浅灰背景 */
  color: #333;
}

.msg-input:focus {
  border-color: #4a90e2; /* 聚焦时边框颜色 */
  background-color: #ffffff;
}

.btn-submit {
  width: 10%;
  margin-left: 10px;
  padding: 12px 20px;
  border: none;
  border-radius: 30px;
  background: linear-gradient(135deg, #4A90E2, #7BBAF9); /* 渐变效果 */
  color: white; /* 确保按钮文字为白色 */
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.btn-submit:hover {
  background: linear-gradient(135deg, #4A90E2, #6ba4f9); /* 悬停时的渐变效果 */
}

.btn-submit:active {
  transform: scale(0.98); /* 按钮点击时轻微缩小 */
}

.footer .msg-input, .footer .btn-submit {
  box-sizing: border-box;
}

.new-conversation-btn {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px; /* 添加一些空间与列表分开 */
  background-color: #007bff;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.3s;
}

.new-conversation-btn:hover {
  background-color: #0056b3; /* 悬停时按钮颜色 */
}

/* 删除按钮 */
.delete-btn {
  font-size: 20px;
  color: #ff4d4f;
  cursor: pointer;
  padding: 0 10px;
  margin-left: 10px;
  display: inline-block;
}

.delete-btn:hover {
  color: #ff3333;
}

.conversation-item-wrapper {
  position: relative;
}

.conversation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.conversation-item-wrapper:hover .conversation-item {
  background-color: #f0f0f0; /* 鼠标悬停时高亮显示 */
}

</style>
