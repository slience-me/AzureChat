from django.db import models

# Create your models here.
# CREATE TABLE users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(32) UNIQUE NOT NULL,
#     password VARCHAR(256) NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=100, null=True, default=None)
    password = models.CharField(verbose_name='密码', max_length=32, null=True, default=None)
    member_type = models.CharField(verbose_name='用户类型', max_length=20, null=True, default='user')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='上次登录时间')

    class Meta:
        db_table = 'member'
        verbose_name_plural = '用户表'

    def __str__(self):
        return f"Member with {self.id} - {self.username}"


class Token(models.Model):
    id = models.AutoField(primary_key=True)
    member_id = models.IntegerField(verbose_name='用户ID', null=True, default=None)
    token_value = models.CharField(verbose_name='签发token', max_length=200, null=True, default=None)
    issued_time = models.DateTimeField(auto_now=True)
    expire_time = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_length=200, null=True, default=None)

    class Meta:
        db_table = 'token'
        verbose_name_plural = '用户Token'

    def __str__(self):
        return f"Member with {self.id} - {self.token_value}"