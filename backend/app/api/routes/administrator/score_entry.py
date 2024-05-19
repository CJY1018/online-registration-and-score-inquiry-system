from typing import List, Optional

from pydantic import BaseModel

from app.api.models.students import Examinees, Exams_name, Students

from fastapi.routing import APIRouter
from tortoise import connections

from fastapi_pagination import Page, paginate, Params, add_pagination
from fastapi import Query, Depends

router = APIRouter()

add_pagination(router)


class ScoreEntry(BaseModel):
    exam_name: str
    exam_turn: int
    id_no: str
    stu_name: str
    exam_grades: Optional[int] = None


def get_pagination_params(
        page: int = Query(1, ge=1),
        per_page: int = Query(20, ge=10, le=100),
):
    return Params(page=page, size=per_page)


@router.get('/administrator/score_entry', response_model=Page[ScoreEntry], tags=['管理员'])
async def get_score_entry(params: Params = Depends(get_pagination_params)):
    conn = connections.get("default")
    examinees = await conn.execute_query_dict(
        'select exams_name.exam_name,examinees.exam_turn,examinees.id_no,students.stu_name,examinees.exam_grades from examinees,exams_name,students where examinees.exam_no = exams_name.exam_no and examinees.id_no = students.id_no')

    paginated_stus = paginate(examinees, params=params)
    return paginated_stus


class ExamineesIn(BaseModel):
    exam_name: str
    exam_turn: int
    id_no: str
    stu_name: str
    exam_grades: Optional[int] = None
    index: int


class ExamineesInList(BaseModel):
    examinees: List[ExamineesIn]


@router.post('/administrator/score_entry')
async def post_score_entry(examinees: ExamineesInList):
    for examinee in examinees.examinees:
        exam_no = await Exams_name.filter(exam_name=examinee.exam_name).first()
        student = await Students.filter(id_no=examinee.id_no).first()
        if not exam_no or not student:
            return {'status': 'failed', 'message': '考试或学生不存在！'}
        await Examinees.filter(exam_no=exam_no.exam_no, exam_turn=examinee.exam_turn, id_no=examinee.id_no).update(
            exam_grades=examinee.exam_grades)

    return {'status': 'success', 'message': '成绩提交成功！'}
