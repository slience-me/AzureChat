import datetime
import json
import uuid

from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from memberManage.jwt_utils import generate_jwt_token
from memberManage.models import Member, Token

def test(requent):
    data = {
        'code': 0,
        'message': '登录成功'
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False),
                        content_type='application/json',
                        charset='utf-8')


def login(request):
    """
        登录功能
    :param request:
    :return:
    """
    data = json.loads(request.body)
    user = data.get("username", '')
    pwd = data.get("password", '')
    print(user, pwd)
    if user == "" or pwd == '':
        print('请填写全部信息！')
        data = {
            'code': 1,
            'message': '请填写全部信息！'
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False),
                            content_type='application/json',
                            charset='utf-8')
    try:
        user = Member.objects.filter(username=user, password=pwd)
        print(user)
        if len(user) == 0:
            print('用户名或者密码错误!')
            data = {
                'code': 1,
                'message': '用户名或者密码错误!!',
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False),
                                content_type='application/json',
                                charset='utf-8')

        # 登录成功状态
        request.session['is_login'] = True
        request.session['usernow'] = user[0].username
        request.session.set_expiry(3 * 24 * 60 * 60)  # 3天
        # 先检查数据库中有没有 有则删除
        tokens = Token.objects.filter(member_id=user[0].id)
        if len(tokens) != 0:
            Token.objects.get(member_id=user[0].id).delete()
        token, issued_time, expire_time = generate_jwt_token(user[0].id)
        data_token = str(uuid.uuid4()).replace('-', '')
        t = {
            'member_id': user[0].id, 'token_value': token,
            'issued_time': issued_time, 'expire_time': expire_time,
            'uuid': data_token
        }
        token_data = Token.objects.create(**t)
        print(token_data)
        print('登录成功')
        user[0].save()
        user[0].password = None
        data = {
            'code': 0,
            'message': '登录成功',
            'user': model_to_dict(user[0]),
            'token': token,
            'key': data_token
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False),
                            content_type='application/json',
                            charset='utf-8')
    except Exception:
        print('登录异常，请稍后再试!')
        data = {
            'code': 1,
            'message': '登录异常，请稍后再试!',
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False),
                            content_type='application/json',
                            charset='utf-8')


def signup(request):
    """
        注册功能
    :param request:
    :return:
    """
    data = json.loads(request.body)
    username = data.get("username", '')
    password = data.get("password", '')
    # member_type = 'user' # user /  admin/ super admin
    if username == '' or password == '':
        print('请填写全部信息！')
        data = {
            'code': 1,
            'message': '请填写全部信息！'
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False),
                            content_type='application/json',
                            charset='utf-8')
    user = Member.objects.filter(username=username)
    if len(user) != 0:
        print('用户已存在')
        data = {
            'code': 1,
            'message': '用户已存在'
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False),
                            content_type='application/json',
                            charset='utf-8')
    else:
        transaction.set_autocommit(False)
        try:
            d = {
                'username': username,
                'password': password,
                'member_type': 'user',
                'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            new_user = Member.objects.create(**d)
            print(new_user)
            data = {
                'code': 0,
                'msg': '注册成功!'
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False),
                                content_type='application/json',
                                charset='utf-8')
        except:
            transaction.rollback()
            # obj = User.objects.get(new_user.username)
            # obj.delete()
            print('事务回滚删除用户')
            print('注册异常，请稍后再试!')
            data = {
                'code': 1,
                'msg': '注册异常，请稍后再试!',
            }
            return HttpResponse(json.dumps(data, ensure_ascii=False),
                                content_type='application/json',
                                charset='utf-8')
        finally:
            transaction.set_autocommit(True)


def logout(request):
    data = json.loads(request.body)
    key = data.get("key", '')
    # try:
    token_obj = Token.objects.get(uuid=key)
    token_obj.delete()
    return HttpResponse(json.dumps({'code': 0, 'message': "注销成功!"}, ensure_ascii=False),
                        content_type='application/json',
                        charset='utf-8')
    # except Exception:
    #     print("注销错误!")
    #     return HttpResponse(json.dumps({'code': 1, 'message': "注销异常，请稍后再试！"}, ensure_ascii=False),
    #                         content_type='application/json',
    #                         charset='utf-8')