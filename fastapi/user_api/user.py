import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from common.user_validation import UserRequest
from common.db_sample import USER_DB 

import uvicorn

app = FastAPI()

# 사용자 정의 예외 처리 함수
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# 간단한 로그인 처리 예시
@app.post("/user")
def join_user(request: UserRequest):
    username = request.username # ID
    password = request.password
    name = request.name
    phone_number = request.phone_number
    dob = request.dob  # 생년월일

    # 중복된 ID 확인
    if username in USER_DB:
        raise HTTPException(status_code=409, detail="이미 존재하는 아이디입니다.")

    # 이름, 전화번호, 생년월일이 동일한 사용자가 있는지 확인
    for user_data in USER_DB.values():
        if user_data["name"] == name and user_data["phone_number"] == phone_number and user_data["dob"] == dob:
            raise HTTPException(status_code=410, detail="이미 가입된 사용자입니다.")

    # 전화번호가 이미 있는지 확인
    if any(user_data["phone_number"] == phone_number for user_data in USER_DB.values()):
        raise HTTPException(status_code=411, detail="이미 존재하는 전화번호입니다.")

    # 사용자 저장
    USER_DB[username] = {
        "name": name,
        "password": password,
        "phone_number": phone_number,
        "dob": dob,
        "ticket_name": []
    }
    
    return {
        "status_code": 0,
        "data": {
            "username": username,
        },
        "message": "signup_success"
    }
#python main.py에서 파일을 불러올 때 Uvicorn서버를 기동
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)