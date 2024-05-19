from fastapi.routing import APIRouter
from app.api.routes import login
from app.api.routes import register
from app.api.routes import test
from app.api.routes import captcha_generator
from app.api.routes import signup
from app.api.routes import pay
from app.api.routes import reset_password
from app.api.routes import score_inquiry
from app.api.routes import upload_picture
from app.api.routes.administrator import registration_information
from app.api.routes.administrator import exam_information
from app.api.routes.administrator import exam_arrangement
from app.api.routes.administrator import score_entry
from app.api.routes.administrator import score_analysis
from app.api.test import insert_db

api_router = APIRouter()

api_router.include_router(login.router, tags=['登录'])
api_router.include_router(register.router, tags=['注册'])
api_router.include_router(captcha_generator.router, tags=['验证码'])
api_router.include_router(signup.router, tags=['报名'])
api_router.include_router(pay.router, tags=['支付'])
api_router.include_router(reset_password.router, tags=['重置密码'])
api_router.include_router(score_inquiry.router, tags=['成绩查询'])
api_router.include_router(upload_picture.router, tags=['上传照片'])
api_router.include_router(registration_information.router, tags=['管理员 - 报名信息'])
api_router.include_router(exam_information.router, tags=['管理员 - 考试信息'])
api_router.include_router(exam_arrangement.router, tags=['管理员 - 考试安排'])
api_router.include_router(score_entry.router, tags=['管理员 - 成绩录入'])
api_router.include_router(score_analysis.router, tags=['管理员 - 成绩分析'])
api_router.include_router(insert_db.router, tags=['测试'])
