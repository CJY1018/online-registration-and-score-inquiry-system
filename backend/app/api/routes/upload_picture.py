import os
from io import BytesIO

import mimetypes
from fastapi import Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from app.api.models.students import Students
from app.api.routes.login import get_current_user
from fastapi.routing import APIRouter

router = APIRouter()


@router.post('/upload_picture')
async def upload_picture(user: Students = Depends(get_current_user), file: UploadFile = File(...)):
    try:
        if user.avatar:
            os.remove(user.avatar)

        file_name = file.filename
        with open(f'./app/avatar/{user.id_no}_{file_name}', 'wb') as f:
            f.write(file.file.read())
        img_path = f'./app/avatar/{user.id_no}_{file_name}'
        await Students.filter(id_no=user.id_no).update(avatar=img_path)
    except Exception as e:
        return {'status': 'failed', 'message': str(e)}
    return {'status': 'success', 'message': '上传成功！'}


@router.get('/get_picture')
async def get_picture(user: Students = Depends(get_current_user)):
    global img
    try:
        img_path = user.avatar
        if not img_path:
            return {'status': 'failed', 'message': '未上传头像！'}
        mime_type, _ = mimetypes.guess_type(img_path)
        # 以流的方式返回图片, 当读取完毕后关闭文件
        with open(img_path, 'rb') as f:
            img = f.read()

        return StreamingResponse(BytesIO(img), media_type=mime_type)
    except Exception as e:
        return {'status': 'failed', 'message': str(e)}
