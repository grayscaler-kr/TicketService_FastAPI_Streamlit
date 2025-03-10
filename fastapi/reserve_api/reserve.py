import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from reservation_validation import DuplicateCheckRequest, ReservationRequest
from common.db_sample import USER_DB
from common.token_auth import decode_access_token

import uvicorn

app = FastAPI()

# HTTPBearer 인스턴스 생성 (Bearer 토큰 사용)
security = HTTPBearer()

# 사용자 정의 예외 처리 함수
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# 인증을 위한 의존성
def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials  # Bearer 토큰 가져오기
    user_info = decode_access_token(token)  # JWT 토큰 디코딩

    if not user_info:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return user_info  # 디코딩된 사용자 정보 반환

# 중복 신청 확인 API
@app.post("/check_duplicate")
def check_duplicate(request: DuplicateCheckRequest, token: str = Depends(get_current_user)):
    if (request.name in USER_DB["name"] and 
        request.phone in USER_DB["phone_number"] and 
        request.dob in USER_DB["dob"]):
        return {"duplicate": True}
    return {"duplicate": False}

@app.post("/verify_user_info")
def verify_user_info(user_info: dict = Depends(get_current_user)):  # 이미 디코딩된 값을 받음
    user_id = user_info.get("sub")  # 토큰에서 가져온 id
    if user_id not in USER_DB:
        return {"user_info_matched": False}

    user_data = USER_DB[user_id]  # 해당 ID의 사용자 정보 가져오기

    return {
        "user_info_matched": True,
        "name": user_data["name"],
        "phone_number": user_data["phone_number"],
        "dob": user_data["dob"],
        "ticket_name": user_data["ticket_name"]
    }

# 예약 신청 API
@app.post("/reserve")
def reserve_ticket(request: ReservationRequest, token: str = Depends(get_current_user)):
    USER_DB["name"].append(request.name)
    USER_DB["phone_number"].append(request.phone)
    USER_DB["dob"].append(request.birth_date)
    USER_DB["ticket_name"].append(request.ticket)
    return {"message": "예약이 완료되었습니다!"}

# python main.py에서 파일을 불러올 때 Uvicorn 서버를 기동
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
