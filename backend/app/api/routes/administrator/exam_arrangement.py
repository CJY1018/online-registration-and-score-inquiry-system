from typing import List, Optional
from app.api.models.students import Invigilators

from pydantic import BaseModel
from tortoise import connections

from app.api.models.students import Examinees
from fastapi.routing import APIRouter

from fastapi_pagination import Page, paginate, Params, add_pagination
from fastapi import Query, Depends


router = APIRouter()

add_pagination(router)


def get_pagination_params(
        page: int = Query(1, ge=1),
        per_page: int = Query(20, ge=10, le=100),
):
    return Params(page=page, size=per_page)


class ExamArrangement(BaseModel):
    id_no: str
    exam_no: int
    exam_turn: int
    exam_name: Optional[str] = None
    invigilator_no: Optional[int] = None
    exam_venue: Optional[str] = None
    exam_venue_no: Optional[int] = None
    exam_grades: Optional[int] = None


@router.get('/administrator/exam_arrangement', response_model=Page[ExamArrangement], tags=['管理员'])
async def get_exam_arrangement(exam_name: Optional[str] = None, exam_turn: Optional[int] = None,
                               params: Params = Depends(get_pagination_params)):
    conn = connections.get("default")
    if not exam_name and not exam_turn:
        stus = await conn.execute_query_dict(
            'select * from exams_name,examinees where exams_name.exam_no = examinees.exam_no')
    elif not exam_name:
        stus = await conn.execute_query_dict(
            'select * from exams_name,examinees where exams_name.exam_no = examinees.exam_no and examinees.exam_turn = %s',
            [exam_turn])
    elif not exam_turn:
        stus = await conn.execute_query_dict(
            'select * from exams_name,examinees where exams_name.exam_no = examinees.exam_no and exams_name.exam_name = %s',
            [exam_name])
    else:
        stus = await conn.execute_query_dict(
            'select * from exams_name,examinees where exams_name.exam_no = examinees.exam_no and exams_name.exam_name = %s and examinees.exam_turn = %s',
            [exam_name, exam_turn])

    # 将查询结果的值转换为字符类型
    for stu in stus:
        stu['exam_no'] = str(stu['exam_no'])
        stu['exam_turn'] = str(stu['exam_turn'])

    paginated_stus = paginate(stus, params=params)
    return paginated_stus


@router.get('/administrator/exam_arrangement/exam_name_turn', tags=['管理员'])
async def get_exam_name_turn():
    conn = connections.get("default")
    stus = await conn.execute_query_dict(
        'select * from exams_name,examinees where exams_name.exam_no = examinees.exam_no')
    # 将考试名称和考试轮次按树形结构组织
    exam_name_turn = {}
    for stu in stus:
        if stu['exam_name'] not in exam_name_turn:
            exam_name_turn[stu['exam_name']] = []
        if stu['exam_turn'] not in exam_name_turn[stu['exam_name']]:
            exam_name_turn[stu['exam_name']].append(stu['exam_turn'])
    return {'status': 'success', 'data': exam_name_turn}


class ExamineesIn(BaseModel):
    id_no: str
    exam_no: int
    exam_turn: int
    exam_name: Optional[str] = None
    invigilator_no: Optional[int] = None
    exam_venue: Optional[str] = None
    exam_venue_no: Optional[int] = None
    exam_grades: Optional[int] = None
    index: int


class ExamineesList(BaseModel):
    exams: List[ExamineesIn]
    page: Optional[int] = None
    per_page: Optional[int] = None


@router.post('/administrator/exam_arrangement')
async def post_exam_arrangement(examinees_list: ExamineesList):
    print(examinees_list.dict())
    # 找到并修改原表数据
    for examinee in examinees_list.dict()['exams']:
        await Examinees.filter(id_no=examinee['id_no'], exam_no=examinee['exam_no'],
                               exam_turn=examinee['exam_turn']).update(invigilator_no=examinee['invigilator_no'],
                                                                       exam_venue=examinee['exam_venue'],
                                                                       exam_venue_no=examinee['exam_venue_no'],
                                                                       exam_grades=examinee['exam_grades'])
    print(examinees_list.page, examinees_list.per_page)
    return {'status': 'success',
            'data': await get_exam_arrangement(params=get_pagination_params(examinees_list.page, examinees_list.per_page))}


@router.get('/administrator/exam_arrangement/invigilator_no')
async def get_exam_arrangement_invigilator():
    invigilators = await Invigilators.all().values('invigilator_no')
    return {'status': 'success', 'data': invigilators}
