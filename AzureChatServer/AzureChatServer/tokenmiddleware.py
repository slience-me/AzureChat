# middleware.py
import json

from django.http import HttpResponse
from memberManage.jwt_utils import verify_jwt_token_only
from memberManage.models import Token


class RequestInterceptorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 在请求到达视图之前执行代码
        allow_path = [
            '/member/login/',
            '/member/signup/',
            '/member/login',
            '/member/signup',
        ]

        # 放行所有以 /admin/ 开头的请求
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        if request.path not in allow_path:
            print(request.headers)
            if "Authorization" in request.headers:
                token = request.headers["Authorization"]
                token = str(token).split(' ')[1]
                if not token:
                    return HttpResponse(json.dumps({'code': 2, 'message': "请求拦截!"}, ensure_ascii=False),
                                        content_type='application/json',
                                        charset='utf-8')
                data = verify_jwt_token_only(token)
                if data:
                    uid = data['user_id']
                    user_token = Token.objects.filter(member_id=uid)
                    # 解析的id和实际的id不等拦截
                    if uid != user_token[0].member_id:
                        return HttpResponse(json.dumps({'code': 2, 'message': "请求拦截!"}, ensure_ascii=False),
                                            content_type='application/json',
                                            charset='utf-8')
                else:
                    print("token无效")
                    return HttpResponse(json.dumps({'code': 2, 'message': "token无效!"}, ensure_ascii=False),
                                        content_type='application/json',
                                        charset='utf-8')

            else:
                return HttpResponse(json.dumps({'code': 2, 'message': "请求拦截!"}, ensure_ascii=False),
                                    content_type='application/json',
                                    charset='utf-8')

        response = self.get_response(request)
        return response
