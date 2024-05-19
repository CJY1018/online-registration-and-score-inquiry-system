from tortoise import connections

from app.api.models.students import Examinees
from fastapi.routing import APIRouter

router = APIRouter()


@router.get('/administrator/score_analysis')
async def get_score_analysis():
    conn = connections.get("default")
    stus = await conn.execute_query_dict(
        'select exam_name,exam_turn from exams_name,examinees where exams_name.exam_no = examinees.exam_no')

    # 将查询结果的值转换为字符类型
    for stu in stus:
        stu['exam_turn'] = str(stu['exam_turn'])

    return {'status': 'success', 'data': stus}


@router.get('/administrator/score_analysis/grades/{exam_name}/{exam_turn}')
async def get_score_analysis_by_exam_name_and_exam_turn(exam_name: str, exam_turn: int):
    conn = connections.get("default")
    grades = await conn.execute_query_dict(
        'select exam_grades from examinees,exams_name where examinees.exam_no = exams_name.exam_no and exams_name.exam_name = %s and examinees.exam_turn = %s',
        [exam_name, exam_turn])
    # 平均分

    # 按成绩直方图显示, 统计各个分数的人数
    grades = [grade['exam_grades'] for grade in grades if grade['exam_grades'] is not None]
    grades = sorted(grades)
    print(grades)
    grades_dict = {}

    total = 0
    count = len(grades)
    if count == 0:
        return {'status': 'failed', 'message': '没有数据！'}

    # 中位数
    median = grades[count // 2] if count % 2 == 1 else (grades[count // 2 - 1] + grades[count // 2]) / 2
    for grade in grades:
        total += grade
        if grade in grades_dict:
            grades_dict[grade] += 1
        else:
            grades_dict[grade] = 1

    for i in range(711):
        if i not in grades_dict:
            grades_dict[i] = 0

    # 保留两位小数
    average = float('%.2f' % (total / count))

    # 按grade升序排列
    grades_dict = dict(sorted(grades_dict.items(), key=lambda x: x[0]))

    grades = [{'grade': str(grade), 'count': count} for grade, count in grades_dict.items()]

    return {'status': 'success', 'data': grades, 'average': average, 'median': median}
