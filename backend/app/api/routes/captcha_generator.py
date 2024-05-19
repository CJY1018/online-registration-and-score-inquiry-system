import random
import string
from typing import Optional

import aioredis

from fastapi.routing import APIRouter
from captcha.image import ImageCaptcha
from fastapi.responses import StreamingResponse

router = APIRouter()

# 生成验证码
@router.get('/captcha/get')
async def get_captcha(captcha_id: Optional[str] = None):
    characters = string.digits + string.ascii_uppercase + string.ascii_lowercase  # 验证码组成，数字+大写字母+小写字母
    char_num = 4
    captcha_str = ''.join(random.sample(characters, char_num))
    print(captcha_str)
    # 保存验证码到redis
    redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    async with redis.client() as conn:
        await conn.set(captcha_id, captcha_str)
        # 设置过期时间
        await conn.expire(captcha_id, 180)

    # 返回验证码图片
    image = ImageCaptcha()
    data = image.generate(captcha_str)
    return StreamingResponse(data, media_type="image/png")


# 验证码校验
@router.get('/captcha/check')
async def check_captcha(captcha_id: str, captcha_code: str):
    redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    print(captcha_id, captcha_code.lower())
    async with redis.client() as conn:
        val = await conn.get(captcha_id)
        if val and val.lower() == captcha_code.lower():
            await conn.delete(captcha_id)
            return {'status': 'success', 'message': '验证码正确！'}
    return {'status': 'failed', 'message': '验证码错误！'}
