# Create your views here.
# views.py
import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

from memberManage.jwt_utils import verify_jwt_token_only
from memberManage.models import Member
from messageManage.azure_openai_client import send_prompt, send_message
from messageManage.models import Conversation, ChatRecord


# def chat():
#     data = request.json
#     user_message = data.get("message", "")
#     if not user_message:
#         return jsonify({"error": "消息不能为空"}), 400
#
#     response = chat_with_gpt(user_message)
#     return jsonify({"response": response})

def create_new_conversation(request):
    authorization_header = request.META.get('HTTP_AUTHORIZATION')
    jwt_data = verify_jwt_token_only(str(authorization_header).split(' ')[1])
    print(jwt_data)
    user_id = jwt_data.get('user_id')
    member = Member.objects.filter(id=user_id)[0]
    conversation = Conversation.objects.create(
        member=member,
        summary='新会话'
    )

    data = {
        "code": 0,
        "message": "success",
        "data": {
            "id": conversation.id,
            "member": conversation.member.username,  # 假设 `username` 是 `Member` 模型的字段
            "summary": conversation.summary
        }
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False),
                        content_type='application/json',
                        charset='utf-8')


def chat_with_openai(request):
    if request.method == 'POST':
        # try:
        data = json.loads(request.body)
        prompt = data.get('prompt', '')
        conversationId = data.get('conversationId', '')

        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        jwt_data = verify_jwt_token_only(str(authorization_header).split(' ')[1])
        print(jwt_data)
        user_id = jwt_data.get('user_id')
        # if type == 'prompt':
        if not prompt:
            return JsonResponse({'code': 1, 'message': '没有输入消息'}, status=400)
        response = send_prompt(prompt)

        data = {
            'code': 0,
            'message': response
        }

        # 对话默认为1
        conversation = Conversation.objects.filter(id=conversationId)[0]
        if conversation is None:
            data = {
                'code': 1,
                'message': 'conversationId异常'
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False),
                                content_type='application/json',
                                charset='utf-8')

        conversation.summary = prompt[:10]
        conversation.save()
        chat_record_user = ChatRecord.objects.create(
            conversation=conversation,
            sender='user',
            message=prompt
        )
        chat_record_assistant = ChatRecord.objects.create(
            conversation=conversation,
            sender='assistant',
            message=response
        )
        return HttpResponse(json.dumps(data, ensure_ascii=False),
                            content_type='application/json',
                            charset='utf-8')



def get_all_conversations(request):
    authorization_header = request.META.get('HTTP_AUTHORIZATION')
    jwt_data = verify_jwt_token_only(str(authorization_header).split(' ')[1])
    print(jwt_data)
    user_id = jwt_data.get('user_id')
    # 获取所有会话记录
    conversations = Conversation.objects.filter(member__id=user_id).values('id', 'member__id', 'member__username', 'summary').order_by('-created_at')
    data = {
        "code": 0,
        "message": "success",
        "data": list(conversations)
    }
    # 返回 JSON 数据
    return HttpResponse(json.dumps(data, ensure_ascii=False),
                            content_type='application/json',
                            charset='utf-8')


def get_chat_records_for_conversation(request, conversation_id):
    try:
        # 获取指定会话的聊天记录
        conversation = Conversation.objects.get(id=conversation_id)
        chat_records = ChatRecord.objects.filter(conversation=conversation).values('sender', 'message').order_by('created_at')
        data = {
            "code": 0,
            "message": "success",
            "data": list(chat_records),
            "conversation_id": conversation.id
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False),
                            content_type='application/json',
                            charset='utf-8')
    except Conversation.DoesNotExist:
        data = {
            "code": 1,
            "message": "Conversation not found",
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False),
                            content_type='application/json',
                            charset='utf-8')


def delete_conversation(request, conversation_id):
    try:
        # 获取指定的 Conversation 对象，若不存在则返回 404 错误
        conversation = get_object_or_404(Conversation, id=conversation_id)
        # 删除 Conversation，自动删除关联的 ChatRecord（因为 on_delete=models.CASCADE）
        conversation.delete()
        # 返回删除成功的响应
        data = {
            "code": 0,
            "message": "删除成功"
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False),
                            content_type='application/json',
                            charset='utf-8')
    except Exception as e:
        # 如果删除失败，返回错误信息
        print(e)
        data = {
            "code": 1,
            "message": "删除失败"
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False),
                            content_type='application/json',
                            charset='utf-8')
