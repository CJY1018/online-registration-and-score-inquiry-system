import os
import hashlib
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.api.models.students import Students

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
# SECRET_KEY = secrets.token_urlsafe(32)
SECRET_KEY = "3a42356f7aef5c270848a7eea08975c7577dc5eb46ebc80f3a57cd9bed341846"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 对密码进行校验
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 获取加密的密码
async def get_password_hash(username: str, password: str) -> str:
    # 查询用户的salt
    user = await Students.get(id_no=username)
    if not user:
        return ''
    # 获取加密密码
    return hashlib.pbkdf2_hmac('sha256', password.strip().encode('utf-8'), bytes.fromhex(user.salt), 100000).hex()
