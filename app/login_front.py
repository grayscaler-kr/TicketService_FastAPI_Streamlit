import streamlit as st
import requests

# FastAPI 서버 URL
FASTAPI_URL = "http://localhost:8000/login"

# Streamlit에서 사용자 입력 받기
st.title("Login Page")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

user_data = {"username": username, "password": password}

if st.button("Login"):
    # FastAPI에 로그인 요청 보내기
    response = requests.post(FASTAPI_URL, json=user_data)
    
    if response.status_code == 200:
        st.success('로그인 성공')  # 로그인 성공
    else:
        error_message = response.json().get("detail", "로그인 실패")

        st.error('로그인 실패')  # 로그인 실패
        # print(data["message"])

if st.button("Join"):
    response = requests.post(FASTAPI_URL, json=user_data)
    print(response)
    if response.status_code == 200:
        st.success("🎉 회원가입 성공! 이제 로그인하세요.")
    else:
        if response.status_code == 602:
            st.error('❌ 회원가입 실패  \n해당ID는 이미 사용중입니다.') 
        elif response.status_code == 422:
            st.error('❌ 회원가입 실패  \nID는 영문과 숫자로만 이루어져야 합니다. 5-20자  \n비밀번호는 최소 1개 이상의 숫자, 영문자, 특수문자를 각각 포함해야 하며 공백을 포함하지 않습니다. 8-30자')
            