from django.contrib import admin

from messageManage.models import Conversation, ChatRecord

# Register your models here.
admin.site.register(Conversation)
admin.site.register(ChatRecord)