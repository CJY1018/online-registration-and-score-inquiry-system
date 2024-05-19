from typing import Optional

from pydantic import BaseModel

from app.api.models.students import Students
from fastapi.routing import APIRouter
from fastapi_pagination import Page, paginate, Params, add_pagination
from fastapi import Query, Depends

from tortoise.expressions import Q

router = APIRouter()

add_pagination(router)


class RegistrationInformation(BaseModel):
    id_no: Optional[str]
    stu_name: Optional[str]
    stu_school: Optional[str]
    stu_department: Optional[str]
    stu_major: Optional[str]
    stu_cls: Optional[str]
    stu_no: Optional[str]
    stu_info: Optional[str]
    pay_status: str
    confirm: str


def get_pagination_params(
        page: int = Query(1, ge=1),
        per_page: int = Query(20, ge=10, le=100),
):
    return Params(page=page, size=per_page)


@router.get('/administrator/registration_information', response_model=Page[RegistrationInformation], tags=['管理员'])
async def get_registration_information(params: Params = Depends(get_pagination_params)):
    stus = await Students.all()
    paginated_stus = paginate(stus, params=params)

    return paginated_stus


@router.get('/administrator/registration_information/search', response_model=Page[RegistrationInformation],
            tags=['管理员'])
async def search_registration_information(id_no: Optional[str] = None,
                                          stu_name: Optional[str] = None,
                                          stu_school: Optional[str] = None,
                                          params: Params = Depends(get_pagination_params)):
    # 模糊查询
    filters = []
    if id_no:
        filters.append(Q(id_no__contains=id_no))
    if stu_name:
        filters.append(Q(stu_name__contains=stu_name))
    if stu_school:
        filters.append(Q(stu_school__contains=stu_school))

    if filters:
        print('aaaaa')
        stus = await Students.filter(*filters).all()
        paginated_stus = paginate(stus, params=params)
        return paginated_stus
    else:
        return await get_registration_information(params=params)
