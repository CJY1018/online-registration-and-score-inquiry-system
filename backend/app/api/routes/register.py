from fastapi.routing import APIRouter
from pydantic import BaseModel
from app.api.models.students import Students
import hashlib
import os

router = APIRouter()


class UserRegisterIn(BaseModel):
    email: str
    id_no: str
    id_type: str
    stu_name: str
    password: str
    salt: str = ''
    tel: str
    pay_status: str = '0'
    confirm: str = '0'


def sha256_salt(password: str):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return key.hex(), salt.hex()


@router.post('/register')
async def register(user_in: UserRegisterIn):
    user = await Students.filter(id_no=user_in.id_no).first()
    if user:
        return {'status': 'failed', 'message': '用户已存在！'}

    # 加密密码
    user_in.password, user_in.salt = sha256_salt(user_in.password)

    await Students.create(**user_in.dict())
    return {'status': 'success', 'message': '用户注册成功！'}
