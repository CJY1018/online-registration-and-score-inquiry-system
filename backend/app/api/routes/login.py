from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel, ValidationError
from app.api.models.students import Students

from app.api.utils import security

router = APIRouter()


class UserLoginIn(BaseModel):
    username: str
    password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/jwt/token')


@router.post('/jwt/token', response_model=security.Token)
async def token_server(user_in: UserLoginIn, resp: Response):
    # 密码sha256加密user_in.password)
    user_in.password = await security.get_password_hash(user_in.username, user_in.password)
    if not user_in.password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='用户不存在!',
                            headers={"WWW-Authenticate": "Bearer"})

    user = await Students.filter(id_no=user_in.username, password=user_in.password).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='用户名或密码错误!',
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(subject=user.id_no, expires_delta=access_token_expires)
    resp.set_cookie(key='access_token', value=access_token, secure=True, samesite='none')
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/jwt/token/admin', response_model=security.Token)
async def token_server(user_in: UserLoginIn, resp: Response):
    # 密码sha256加密user_in.password)
    user_in.password = await security.get_password_hash(user_in.username, user_in.password)
    if not user_in.password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='用户不存在!',
                            headers={"WWW-Authenticate": "Bearer"})

    user = await Students.filter(id_no=user_in.username, password=user_in.password).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='用户名或密码错误!',
                            headers={"WWW-Authenticate": "Bearer"})
    print('kkk')
    if user.id_no != '362502200210180012':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权限登录!")
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(subject=user.id_no, expires_delta=access_token_expires)
    resp.set_cookie(key='admin_token', value=access_token, secure=True, samesite='none')
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Students:
    try:
        payload = jwt.decode(token=token, key=security.SECRET_KEY, algorithms=[security.ALGORITHM])
        id_no = payload.get('sub')
    except (JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无法验证凭据!")

    user = await Students.filter(id_no=id_no).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="找不到该用户!")
    return user


@router.get('/signup_info')
async def me(user: Students = Depends(get_current_user)):
    dict(user).pop('password')
    dict(user).pop('salt')
    return dict(user)


@router.get('/administrator_info')
async def me(user: Students = Depends(get_current_user)):
    if user.id_no != '362502200210180012':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权限查看!")
    dict(user).pop('password')
    return dict(user)
