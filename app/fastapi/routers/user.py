# fastapi-app/routers/user.py
from fastapi import APIRouter, HTTPException
from models import UserRequest
from db_sample import USER_DB  

router = APIRouter()

# 사용자 생성 (회원가입)
@router.post("/user")
def join_user(request: UserRequest):
    username = request.username
    password = request.password

    # 중복된 ID 확인
    if username in USER_DB:
        raise HTTPException(detail="이미 존재하는 아이디입니다.")

    # 사용자 저장
    USER_DB[username] = password
    return {
        "status_code": 0,
        "data": {
            "username": username,
        },
        "message": "signup_success"
    }
