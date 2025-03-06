from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, Field, field_validator
import re

#POST: 데이터 생성
#GET: 데이터 표시
#PUT: 데이터 갱신
#DELETE: 데이터 삭제

#FastAPI인스턴스 생성
app = FastAPI()

# 임시 사용자 데이터
USER_DB = {
    "testuser": "Test@1234",  # 저장된 비밀번호
}

class UserRequest(BaseModel):
    username: str = Field(..., min_length=5, max_length=20)  # ID 길이 제한 (5~20자)
    password: str = Field(..., min_length=8, max_length=30)  # 비밀번호 길이 제한 (8~30자)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not v.isalnum():  # 영문+숫자로만 이루어져야 함
            raise ValueError("ID는 영문과 숫자로만 이루어져야 합니다.")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not any(c.isdigit() for c in v):
            raise ValueError("비밀번호는 최소 1개 이상의 숫자를 포함해야 합니다.")
        if not any(c.isalpha() for c in v):
            raise ValueError("비밀번호는 최소 1개 이상의 영문자를 포함해야 합니다.")
        if " " in v:
            raise ValueError("비밀번호는 공백을 포함할 수 없습니다.")
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/|`~]', v):
            raise ValueError("비밀번호는 최소 1개 이상의 특수문자를 포함해야 합니다.")
        return v


@app.get("/")
def read_root():
    return {"message": "Welcome to the main page!"}

@app.post("/login")
async def login(request: UserRequest):
    username = request.username
    password = request.password

    # ID 존재 여부 확인
    if username not in USER_DB:
        raise HTTPException(status_code=600, detail="존재하지 않는 아이디입니다.")

    # 비밀번호 검증
    if USER_DB[username] != password:
        raise HTTPException(status_code=601, detail="비밀번호가 틀렸습니다.")

    return {
                "status_code": 0,
                "data": {
                    "username": username
                },
                "message": "login_success"}

@app.post("/join")
def join_user(request: UserRequest):
    username = request.username
    password = request.password

    # 중복된 ID 확인
    if username in USER_DB:
        raise HTTPException(status_code=602, detail="이미 존재하는 아이디입니다.")

    # 사용자 저장
    USER_DB[username] = password
    return {
        "status_code": 0,
        "data": {
            "username": username,
        },
        "message": "signup_success"
    }


@app.get("/main")
def main_page():
    return {"message": "This is the main page."}

#python main.py에서 파일을 불러올 때 Uvicorn서버를 기동
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)