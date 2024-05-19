from app.api.routes.login import get_current_user
from app.api.models.students import Students
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter()


class StudentsExtra(BaseModel):
    stu_school: str
    stu_department: Optional[str] = None
    stu_major: Optional[str] = None
    stu_cls: str
    stu_no: str
    stu_info: Optional[str] = None
    confirm: str


@router.post('/signup')
async def signup(student_extra: StudentsExtra, student: Students = Depends(get_current_user)):
    try:
        await Students.filter(id_no=student.id_no).update(**student_extra.dict())
    except Exception as e:
        print(e)
        return {'status': 'failed', 'message': '报名信息提交失败！'}
    return {'status': 'success', 'message': '报名信息提交成功！'}
