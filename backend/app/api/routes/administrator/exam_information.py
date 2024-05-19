from typing import List, Optional, Any
import datetime
import pandas as pd

from tortoise.transactions import atomic

from app.api.models.students import Exams_info, Exams_name

from fastapi import Body
from pydantic import BaseModel
from tortoise import connections

from fastapi.routing import APIRouter

router = APIRouter()


@router.get('/administrator/exam_information')
async def get_exam_information():
    # 'select exams_name.exam_name,exams_info.exam_time from exams_info,exams_name where exams_info.exam_no = exams_name.exam_no')
    conn = connections.get("default")
    stus = await conn.execute_query_dict(
        'select * from exams_info,exams_name where exams_info.exam_no = exams_name.exam_no')

    # 将查询结果的值转换为字符类型
    for stu in stus:
        stu['exam_no'] = str(stu['exam_no'])
        stu['exam_turn'] = str(stu['exam_turn'])
    return {'status': 'success', 'data': stus}


class Exam(BaseModel):
    exam_no: int
    exam_turn: int
    exam_time: datetime.datetime
    exam_info: Optional[str] = None
    exam_name: str
    index: int


class Exams(BaseModel):
    exams: List[Exam]


@atomic()
async def exam_information(exams: Exams):
    # 事务操作, 先获取原表数据
    exams_info_all = await Exams_info.all()
    exams_name_all = await Exams_name.all()
    exams_name_all_dict = {}
    # 将exams_name_all转换为字典
    for exam_name in exams_name_all:
        exams_name_all_dict[exam_name.exam_no] = exam_name.exam_name

    # 转换为DataFrame
    exams_info_df = pd.DataFrame([dict(exam) for exam in exams_info_all])
    # 然后将新数据转换为DataFrame, 并删除index列
    exams_df = pd.DataFrame(exams.dict()['exams'])
    exams_df = exams_df.drop(columns='index')

    # 先计算原数据和新数据的差集
    # 通过outer join, 然后取出原数据中没有的数据
    diff = pd.merge(exams_info_df, exams_df, on=['exam_no', 'exam_turn'], how='outer', indicator=True,
                    validate="many_to_many")
    diff_left = diff[diff['_merge'] == 'left_only']

    # 然后计算新数据和原数据的差集
    # 通过outer join, 然后取出新数据中没有的数据
    diff_right = diff[diff['_merge'] == 'right_only']
    # 判断exam_no是否与exams_name相对应
    for index, row in diff_right.iterrows():
        if row['exam_name'] != exams_name_all_dict[row['exam_no']]:
            return {'status': 'failed', 'message': '考试名称不合法！'}

    # 再计算新数据和原数据的交集
    # 通过inner join, 然后取出新数据和原数据都有的数据
    diff_inner = diff[diff['_merge'] == 'both']
    # 判断exam_no是否与exams_name相对应
    for index, row in diff_inner.iterrows():
        if row['exam_name'] != exams_name_all_dict[row['exam_no']]:
            return {'status': 'failed', 'message': '考试名称不合法！'}
    print(diff_inner[['exam_no', 'exam_turn']])
    # 判断diff_inner[['exam_no', 'exam_turn']]是否有重复
    if diff_inner[['exam_no', 'exam_turn']].duplicated().any():
        return {'status': 'failed', 'message': '当考试编号相同时，考试场次不能相同！'}

    # 将新数据中没有的数据插入到数据库中
    for index, row in diff_right.iterrows():
        await Exams_info.create(exam_no=row['exam_no'], exam_turn=row['exam_turn'], exam_time=row['exam_time_y'],
                                exam_info=row['exam_info_y'])

    # 将原数据中有而新数据中没有的数据删除
    for index, row in diff_left.iterrows():
        await Exams_info.filter(exam_no=row['exam_no'], exam_turn=row['exam_turn']).delete()

    # 将原数据和新数据都有的数据更新
    for index, row in diff_inner.iterrows():
        await Exams_info.filter(exam_no=row['exam_no'], exam_turn=row['exam_turn']).update(
            exam_time=row['exam_time_y'], exam_info=row['exam_info_y'])

    return {'status': 'success', 'message': '考试安排提交成功！'}


@router.post('/administrator/exam_information')
async def post_exam_information(exams: Exams):
    try:
        return await exam_information(exams)
    except Exception as e:
        print(e)
        return {'status': 'failed', 'message': '考试安排提交失败！'}
