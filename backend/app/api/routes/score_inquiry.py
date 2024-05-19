from pydantic import BaseModel
from tortoise import connections

from app.api.models.students import Students, Examinees, Exams_name
from app.api.routes.login import get_current_user

from fastapi.routing import APIRouter
from fastapi import Depends

EXAM_NAME_CN = {'CET 4': '全国大学英语四级考试(CET4)成绩列表',
                'CET 6': '全国大学英语六级考试(CET6)成绩列表'}

router = APIRouter()


@router.get('/score_inquiry')
async def get_exam_name(user: Students = Depends(get_current_user)):
    try:
        exam_name_map = {}
        for i in await Exams_name.all():
            exam_name_map[i.exam_no] = i.exam_name

        exam_no = await Examinees.filter(id_no=user.id_no).values('exam_no')
        exam_names = []
        for i in exam_no:
            exam_names.append(exam_name_map[i['exam_no']])
    except Exception as e:
        return {'status': 'failed', 'message': str(e)}

    return {'status': 'success', 'exam_names': list(set(exam_names)), 'stu_name': user.stu_name, 'id_no': user.id_no}


class ScoreInquiryOut(BaseModel):
    exam_turn: int
    exam_grades: int
    stu_school: str
    rank: int
    school_rank: int


@router.get('/score_inquiry/exams/{exam_name}')
async def get_exams(exam_name: str, user: Students = Depends(get_current_user)):
    exam_no = dict(await Exams_name.get(exam_name=exam_name).values('exam_no'))['exam_no']
    examinees = list(
        await Examinees.filter(id_no=user.id_no, exam_no=exam_no).values('exam_turn', 'exam_grades'))
    score_inquiry_out_list = []
    conn = connections.get("default")
    print(examinees)

    for i in examinees:
        if not i['exam_grades']:
            continue
        # 总排名
        rank = await Examinees.filter(exam_no=exam_no, exam_turn=i['exam_turn'],
                                      exam_grades__gt=i['exam_grades']).count()
        # 本校排名
        school_rank = await conn.execute_query_dict(
            'select count(*) from examinees,students where examinees.id_no = students.id_no '
            'and exam_no = %s and exam_turn = %s and exam_grades > %s and stu_school = %s',
            [exam_no, i['exam_turn'], i['exam_grades'], user.stu_school])
        score_inquiry_out_list.append(
            ScoreInquiryOut(exam_turn=i['exam_turn'], exam_grades=i['exam_grades'], stu_school=user.stu_school,
                            rank=rank + 1, school_rank=school_rank[0]['count(*)'] + 1))

    return {'status': 'success', 'data': score_inquiry_out_list, 'exam_title': EXAM_NAME_CN[exam_name]}
