# fastapi-app/routers/login.py
from fastapi import APIRouter, HTTPException
from token_auth import create_access_token
from fastapi.responses import JSONResponse
from models import UserRequest
from db_sample import USER_DB  

router = APIRouter()

# 간단한 로그인 처리 예시
@router.post("/login")
async def login(request: UserRequest):
    # ID 존재 여부 확인
    if request.username not in USER_DB:
        raise HTTPException(detail="존재하지 않는 아이디입니다.")
    
    # 비밀번호 검증
    if USER_DB[request.username] != request.password:
        raise HTTPException(detail="비밀번호가 틀렸습니다.")
    
    # JWT 토큰 생성
    user_data = {"sub": request.username}
    access_token = create_access_token(user_data)

    # JSONResponse 객체 생성
    response_data = {"access_token": access_token}

    response = JSONResponse(content=response_data)
    
    # 쿠키에 토큰 저장
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="None", secure=True)

    return response




