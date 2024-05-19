import datetime
import time
import hashlib
import requests
import random

from typing import Optional
from fastapi import Depends
from pydantic import BaseModel

from app.api.routes.login import get_current_user
from app.api.models.students import Examinees, Exams_name, Students, Exams_info
from fastapi.routing import APIRouter

router = APIRouter()


@router.get('/afdian')
async def afdian(page):
    ts = int(time.time())
    token = "pWM7SPKhdmCDR3TgNrBn8EJsVxjfv9Hk"
    user_id = "411df852571311ea95e852540025c377"
    md5_str = token + 'params{"page":%s}ts' % page + str(ts) + 'user_id' + user_id
    md5 = hashlib.md5(md5_str.encode(encoding='UTF-8')).hexdigest()
    # 请求https://afdian.net/api/open/query-order
    url = "https://afdian.net/api/open/query-order"
    headers = {
        "Authorization": "Bearer " + token
    }
    params = {
        "user_id": user_id,
        "params": "{\"page\":%s}" % page,
        "ts": ts,
        "sign": md5
    }
    response = requests.get(url, headers=headers, params=params)

    examinees_in = []

    exam_name_map = {}
    for i in await Exams_name.all():
        exam_name_map[i.exam_name] = i.exam_no

    for i in response.json()['data']['list']:
        for j in i['sku_detail']:
            if j['name'] in exam_name_map and i['remark'] != '':
                examinees_in.append(
                    Examinees(id_no=i['remark'],
                              exam_no=exam_name_map[j['name']],
                              exam_turn=random.randint(1, 2)))
    print(examinees_in)
    # 当数据库中没有数据时，才插入数据
    for i in examinees_in:
        if not await Examinees.filter(id_no=i.id_no, exam_no=i.exam_no, exam_turn=i.exam_turn).first():
            await Examinees.create(**dict(i))
            await Students.filter(id_no=i.id_no).update(pay_status='1')

    return response.json()


class PayOut(BaseModel):
    exam_name: str
    exam_price: float
    exam_venue: Optional[str] = None
    exam_venue_no: Optional[int] = None
    exam_time: Optional[datetime.datetime] = None
    exam_info: Optional[str] = None


@router.get('/pay')
async def pay(user=Depends(get_current_user)):
    # 查询爱发电订单接口，获取支付信息
    await afdian(1)
    # 查询身份证号为user.id_no的学生是否支付
    stu = await Students.filter(id_no=user.id_no, pay_status='1', confirm='1')
    if not stu:
        return {'status': 'failed', 'message': '未支付!'}

    # 若支付成功，查询考试信息
    examinees = await Examinees.get(id_no=user.id_no, exam_turn=1).values('exam_no', 'exam_turn', 'exam_venue',
                                                                          'exam_venue_no')
    print(examinees)
    exam_name_map = {}
    for i in await Exams_name.all():
        exam_name_map[i.exam_no] = i.exam_name

    exam_time, exam_info = dict(
        await Exams_info.get(exam_no=examinees['exam_no'], exam_turn=examinees['exam_turn']).values(
            'exam_time',
            'exam_info')).values()
    exam_time = exam_time.strftime('%Y-%m-%d %H:%M:%S')

    pay_out = PayOut(exam_name=exam_name_map[examinees['exam_no']],
                     exam_price=examinees['exam_no'] == 1 and 1.5 or 1,
                     exam_venue=examinees['exam_venue'],
                     exam_venue_no=examinees['exam_venue_no'],
                     exam_time=exam_time,
                     exam_info=exam_info)

    return {'status': 'success', 'data': pay_out}
