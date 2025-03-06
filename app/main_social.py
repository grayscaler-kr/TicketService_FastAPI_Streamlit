from fastapi import FastAPI, Depends, Request, HTTPException
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
import os
import secrets

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="dkagh1.")

# OAuth2 클라이언트 설정 (카카오)
oauth = OAuth()
oauth.register(
    name='kakao',
    client_id="b87e11a976515ec3ea2cd2cadbda1698",
    client_secret="PvW1BZrT4OClMXAUgoB95jqLHop6UVvY",
    authorize_url="https://kauth.kakao.com/oauth/authorize",
    access_token_url="https://kauth.kakao.com/oauth/token",
    refresh_token_url=None,
    # client_kwargs={"scope": "profile_nickname", "state": "12345"}
)
# oauth.register(
#     name='kakao',
#     client_id=os.getenv('KAKAO_CLIENT_ID'),
#     client_secret=os.getenv('KAKAO_CLIENT_SECRET'),
#     authorize_url="https://kauth.kakao.com/oauth/authorize",
#     access_token_url="https://kauth.kakao.com/oauth/token",
#     refresh_token_url=None,
#     client_kwargs={"scope": "profile", "state": "12345"}
# )
# 카카오 로그인 페이지
@app.get("/kakao_login")
async def login(request: Request):
    state = secrets.token_urlsafe(32)  # 고유한 state 값을 생성
    request.session['state'] = state   # 세션에 저장
    redirect_uri = "http://localhost:8000/auth"  # 인증 후 리디렉션 받을 URL    # redirect_uri = url_for('auth', _external=True)
    return await oauth.kakao.authorize_redirect(request, redirect_uri, state=state)

# 카카오 인증 후 처리
@app.route("/auth")
async def auth(request: Request):
    saved_state = request.session.get('state')
    if not saved_state:
        raise HTTPException(status_code=400, detail="State not found")

    # 카카오에서 돌아온 state와 세션의 state를 비교
    state = request.query_params.get('state')
    if state != saved_state:
        raise HTTPException(status_code=400, detail="CSRF verification failed")

    try:
        # 카카오에서 받은 인증 코드로 액세스 토큰을 받아옵니다.
        token = await oauth.kakao.authorize_access_token(request)
        # 토큰을 사용하여 사용자 정보 가져오기
        user_info = await oauth.kakao.parse_id_token(request)
        return {"user_info": user_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during Kakao login: {str(e)}")

# 메인 페이지 (로그인 처리 후 접근)
@app.get("/main")
def main():
    return {"message": "This is the main page."}

# FastAPI 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
