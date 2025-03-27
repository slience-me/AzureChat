# urls.py
from django.urls import path

from messageManage import views

urlpatterns = [
    path('chat/', views.chat_with_openai, name='chat_with_openai'),
    path('conversations/', views.get_all_conversations, name='conversation_list'),
    path('conversations/new', views.create_new_conversation, name='conversation_add'),
    path('conversations/<int:conversation_id>/del/', views.delete_conversation, name='delete_conversation'),
    path('conversations/<int:conversation_id>/chat_records/', views.get_chat_records_for_conversation, name='chat_record_list')
]
