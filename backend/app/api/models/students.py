from tortoise.models import Model
from tortoise import fields


class Students(Model):
    id_no = fields.CharField(max_length=18, pk=True)
    id_type = fields.CharField(max_length=1)
    email = fields.CharField(max_length=30)
    tel = fields.CharField(max_length=11)
    avatar = fields.CharField(max_length=255, null=True)
    stu_no = fields.CharField(max_length=30, null=True)
    stu_name = fields.CharField(max_length=20)
    stu_school = fields.CharField(max_length=30, null=True)
    stu_department = fields.CharField(max_length=30, null=True)
    stu_major = fields.CharField(max_length=30, null=True)
    stu_cls = fields.CharField(max_length=30, null=True)
    stu_info = fields.CharField(max_length=255, null=True)
    password = fields.CharField(max_length=255)
    salt = fields.CharField(max_length=255, null=True)
    confirm = fields.CharField(max_length=1)
    pay_status = fields.CharField(max_length=1)


class Exams_info(Model):
    exam_no = fields.IntField(pk=True)
    exam_turn = fields.IntField()
    exam_info = fields.CharField(max_length=60, null=True)
    exam_time = fields.TimeField()


class Exams_name(Model):
    exam_no = fields.IntField(pk=True)
    exam_name = fields.CharField(max_length=30)


class Examinees(Model):
    id_no = fields.CharField(max_length=18, pk=True)
    exam_no = fields.IntField()
    exam_turn = fields.IntField()
    invigilator_no = fields.IntField(null=True)
    exam_venue = fields.CharField(max_length=60, null=True)
    exam_venue_no = fields.IntField(null=True)
    exam_grades = fields.SmallIntField(null=True)


class Invigilators(Model):
    invigilator_no = fields.IntField(pk=True)
    invigilator_name = fields.CharField(max_length=20)
