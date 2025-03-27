from django.contrib import admin

from memberManage.models import Member, Token

# Register your models here.

admin.site.register(Member)
admin.site.register(Token)