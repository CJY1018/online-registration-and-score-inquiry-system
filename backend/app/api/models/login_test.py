from tortoise.models import Model
from tortoise import fields


class User(Model):
    id_no = fields.CharField(pk=True, max_length=10)
    password = fields.CharField(max_length=20)
