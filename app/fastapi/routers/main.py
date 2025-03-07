# fastapi-app/routers/main.py
from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.get("/main")
async def read_main(request: Request):
    # 쿠키에서 토큰을 가져오기
    pass
