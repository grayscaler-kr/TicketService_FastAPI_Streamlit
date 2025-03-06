import streamlit as st
import requests

# FastAPI 서버 URL (로그인 엔드포인트)
FASTAPI_URL = "http://192.168.108.40:8000/login"

# Streamlit에서 사용자 입력 받기
st.title("Login Page")

username = st.text_input("Username")
password = st.text_input("Password", type="password")


if st.button("Login with Kakao"):
    # FastAPI에 Kakao 로그인 요청 보내기 (유사한 방식으로)
    response = requests.get("http://192.168.108.40:8000/kakao_login")  # Kakao 엔드포인트 추가
    print(response)
    if response.status_code == 200:
        st.success("Successfully logged in with Kakao!")
        st.write(response.text)  # 인증된 사용자 정보 표시
    else:
        st.error("Kakao login failed!")
