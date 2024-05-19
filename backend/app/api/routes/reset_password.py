import io
from app.api.models.students import Students
from app.api.routes.register import sha256_salt

from fastapi.routing import APIRouter
from fastapi import Request
import smtplib
import email.utils
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase

import aioredis

from PIL import Image, ImageDraw, ImageFont
import random

from pydantic import BaseModel

router = APIRouter()

sender = '1310825002@qq.com'


class UserEmailIn(BaseModel):
    email: str


# 生成验证码图片
def generate_captcha() -> (str, io.BytesIO):
    # 生成验证码
    captcha = ''
    for _ in range(6):
        captcha += str(random.randint(0, 9))

    # 生成图片
    width, height = 190, 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial.ttf', 36)
    for i in range(6):
        draw.text((10 + i * 30, 10), captcha[i], font=font, fill=(0, 0, 0))

    # 保存为png格式到io流
    image_bytes_io = io.BytesIO()
    image.save(image_bytes_io, format='PNG')

    return captcha, image_bytes_io


# 发送邮件
@router.post('/reset_password/send_email')
async def reset_password(user_in: UserEmailIn, request: Request):
    # 编辑邮件内容
    mail = MIMEMultipart()
    mail['To'] = email.utils.formataddr((user_in.email, user_in.email))
    mail['From'] = email.utils.formataddr(('CJY.', sender))
    mail['Subject'] = '[CET 报名系统] 重置密码'

    # 生成验证码
    captcha, image_bytes_io = generate_captcha()
    image = MIMEImage(image_bytes_io.getvalue())
    mail.attach(image)
    image.add_header('Content-ID', 'captcha')

    mail_content = f"""
            <html>
              <body>
                <p style="font-size: 20px;background-color: #00AEEC;color: white;padding: 10px 0;">CET报名系统</p>
                <h3>尊敬的用户：</h3>
                <p>您好！您正在进行密码重置操作，验证码为：</p>
                <img src="cid:captcha" alt="captcha" style="display: block;margin: 10px auto;">
                <p>请在 10 分钟内输入验证码以完成密码重置。</p>
                <p>如非本人操作，请忽略此邮件。</p>
                <p>祝您生活愉快！</p>
                <br><br>
                <p>此密码重置请求来自IP地址：{request.client.host}</p>
                <p style="text-align: right;">BY: CJY.</p>
              </body>
            </html>
        """
    mail.attach(MIMEText(mail_content, 'html', 'utf-8'))

    # 发送邮件
    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login(sender, 'jwgpycfedmbthjcj')
    server.set_debuglevel(True)
    try:
        server.sendmail(sender, [user_in.email], msg=mail.as_string())
        # 将验证码存入redis
        redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
        async with redis.client() as conn:
            await conn.set(user_in.email, captcha)
            await conn.expire(user_in.email, 600)

    except Exception:
        return {'status': 'failed', 'message': '邮件发送失败！'}

    finally:
        server.quit()

    return {'status': 'success', 'message': '验证码已发送至您的邮箱！'}


class UserCaptchaIn(BaseModel):
    email: str
    captcha: str


# 校验验证码
@router.post('/reset_password/check_captcha')
async def check_captcha(user_in: UserCaptchaIn):
    redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    async with redis.client() as conn:
        val = await conn.get(user_in.email)
        if val and val == user_in.captcha:
            await conn.delete(user_in.email)
            return {'status': 'success', 'message': '验证码正确！'}
    return {'status': 'failed', 'message': '验证码错误！'}


class UserPasswordIn(BaseModel):
    email: str
    password: str
    id_no: str


# 重置密码
@router.post('/reset_password')
async def reset_password(user_in: UserPasswordIn):
    try:
        stu = await Students.filter(email=user_in.email, id_no=user_in.id_no).first()
        if not stu:
            return {'status': 'failed', 'message': '身份证号码不匹配！'}

        # 将新密码加密
        password, salt = sha256_salt(user_in.password)
        # 更新数据库
        await Students.filter(email=user_in.email).update(password=password, salt=salt)
    except Exception:
        return {'status': 'failed', 'message': '密码重置失败！'}
    return {'status': 'success', 'message': '密码重置成功！'}
