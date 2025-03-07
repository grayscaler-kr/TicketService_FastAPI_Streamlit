# fastapi-app/main.py
import sys, os

# app/fastapi-app/ 상대 경로로 routers 디렉토리가 포함된 디렉토리 경로 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../fastapi-app')))

from fastapi import FastAPI
from routers import login, user, main, reserve
import uvicorn

app = FastAPI()


# 라우터 등록
app.include_router(login.router, prefix="", tags=["auth"])
app.include_router(user.router, prefix="", tags=["users"])
app.include_router(main.router, prefix="", tags=["main"])
app.include_router(reserve.router, prefix="", tags=["reservations"])
app.include_router(reserve.router, prefix="", tags=["verify_token"])


#python main.py에서 파일을 불러올 때 Uvicorn서버를 기동
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)