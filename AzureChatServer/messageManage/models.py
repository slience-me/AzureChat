from django.db import models

from memberManage.models import Member


# Create your models here.

# CREATE TABLE conversations (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT,
#     summary VARCHAR(10),
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES users(id)
# );
#
# CREATE TABLE chat_records (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     conversation_id INT,
#     sender VARCHAR(32),
#     message TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (conversation_id) REFERENCES conversations(id)
# );


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    summary = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation with {self.member.username} - {self.summary}"

    class Meta:
        db_table = 'conversation'
        verbose_name_plural = '会话表'

class ChatRecord(models.Model):
    id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.CharField(max_length=32)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} in conversation {self.conversation.id}"

    class Meta:
        db_table = 'chat_record'
        verbose_name_plural = '聊天记录表'