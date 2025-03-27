import time
# pip3 install pyjwt
import jwt
import time
from datetime import datetime

JWT_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24 * 3  # token有效时间
JWT_TOKEN_SECRET_SALT = 'salt.2023.10.14'
JWT_TOKEN_ALGORITHM = 'HS256'  # HASH算法


def sTodate(timestamp):
    """
        时间戳转日期时间 %Y-%m-%d %H:%M:%S
    :param timestamp: 当前时间戳
    :return:
    """
    # 使用datetime模块将时间戳转换为日期时间对象
    dt_object = datetime.fromtimestamp(timestamp)
    # 格式化日期时间对象为字符串
    formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    # print(formatted_date)
    return formatted_date


def generate_jwt_token(user):
    """根据用户id生成token"""
    local_time = int(time.time())
    data = {'user_id': user, 'exp': local_time + JWT_TOKEN_EXPIRE_SECONDS}
    # print("generate data:", data)
    jwtToken = jwt.encode(data, JWT_TOKEN_SECRET_SALT, algorithm=JWT_TOKEN_ALGORITHM)
    date_time = sTodate(local_time)
    expire_time = sTodate(local_time + JWT_TOKEN_EXPIRE_SECONDS)
    return jwtToken, date_time, expire_time


def verify_jwt_token(user: str, jwtToken: str) -> bool:
    """验证用户token"""
    data = {'user_id': user}
    try:
        payload = jwt.decode(jwtToken, JWT_TOKEN_SECRET_SALT, algorithms=[JWT_TOKEN_ALGORITHM])
        print("verify:", payload)
        exp = int(payload.pop('exp'))
        if time.time() > exp:
            print('已失效')
            return False
        return data == payload
    except jwt.exceptions.ExpiredSignatureError as ex:
        print('token签名过期:', ex)
    except jwt.PyJWTError as ex:
        print('token解析失败:', ex)
    return False


def verify_jwt_token_only(jwtToken: str):
    try:
        payload = jwt.decode(jwtToken, JWT_TOKEN_SECRET_SALT, algorithms=[JWT_TOKEN_ALGORITHM])
        print("verify:", payload)
        exp = int(payload.pop('exp'))
        if time.time() > exp:
            print('已失效')
            return None
        return payload
    except jwt.exceptions.ExpiredSignatureError as ex:
        print('token签名过期:', ex)
    except jwt.PyJWTError as ex:
        print('token解析失败:', ex)
    return None