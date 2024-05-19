import random
import numpy as np
from app.api.routes.register import sha256_salt
from app.api.models.students import Students, Exams_info, Exams_name, Examinees, Invigilators

from fastapi.routing import APIRouter
from faker import Faker

router = APIRouter()


@router.get('/insert_db')
async def insert_db():
    # 配置中文
    fake = Faker(locale='zh_CN')
    exams_no_turn = await Exams_info.all().values('exam_no', 'exam_turn')
    exams_no_turn_map = {}
    for exam in exams_no_turn:
        if exam['exam_no'] not in exams_no_turn_map:
            exams_no_turn_map[exam['exam_no']] = []
        exams_no_turn_map[exam['exam_no']].append(exam['exam_turn'])

    invigilators = list(await Invigilators.all().values('invigilator_no'))
    invigilators = [dict(invigilator)['invigilator_no'] for invigilator in invigilators]

    student_list = []
    examinees_list = []

    # 生成正态分布的考试成绩, 均值425, 标准差95
    normal_grades = np.random.normal(425, 95, 1000)
    for _ in range(10000):
        id_no = fake.ssn(min_age=16, max_age=35)  # 身份证号
        password, salt = sha256_salt(fake.password())  # 密码
        confirm = random.randint(0, 1)  # 是否确认
        pay_status = 0 if confirm == 0 else random.randint(0, 1)  # 是否支付

        student_list.append(Students(
            id_no=id_no,
            id_type=random.randint(1, 9),
            email=fake.email(),
            tel=fake.phone_number(),
            stu_name=fake.name(),
            password=password,
            salt=salt,
            confirm=confirm,
            pay_status=pay_status))

        exam_no = random.choice(list(exams_no_turn_map.keys()))  # 考试编号
        exam_turn = random.choice(exams_no_turn_map[exam_no])  # 考试轮次
        exam_grades = int(normal_grades[random.randint(0, 999)] % 710)  # 考试成绩, 范围在0-710之间
        examinees_list.append(Examinees(
            id_no=id_no,
            exam_no=exam_no,
            exam_turn=exam_turn,
            invigilator_no=random.choice(invigilators),
            exam_grades=exam_grades))

    await Students.bulk_create(student_list)
    await Examinees.bulk_create(examinees_list)
