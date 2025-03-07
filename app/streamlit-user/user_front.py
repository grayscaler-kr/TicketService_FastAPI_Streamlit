import configparser
import streamlit as st
import requests

config = configparser.ConfigParser()
config.read('/test-FastAPI/app/config.ini')

# URL 가져오기
USER_URL = config['FASTAPI_URL']['USER_URL']

# streamlit main url - front connect
LOGIN_URL = config['STREAMLIT_URL']['LOGIN_URL']


# 회원가입 페이지
st.title("회원가입 페이지")

# 아이디와 비밀번호 입력
username = st.text_input("아이디")
password = st.text_input("비밀번호", type="password")
password_confirm = st.text_input("비밀번호 확인", type="password")

# 가입 버튼
if st.button("회원가입"):
    # 입력 값 확인
    if username and password and password_confirm:
        if password == password_confirm:
            # 가입 정보를 FastAPI 서버로 전송
            url = USER_URL  # FastAPI 서버 URL (회원가입 엔드포인트)
            data = {
                "username": username,
                "password": password
            }

            # POST 요청을 보내고 응답 받기
            response = requests.post(url, json=data)

            if response.status_code == 200:
                st.success('회원가입 성공')  # 회원가입 성공 메시지
                # 로그인 페이지로 리다이렉션
                st.markdown(f'<meta http-equiv="refresh" content="0; url={LOGIN_URL}">', unsafe_allow_html=True)
            else:
                st.error('회원가입 실패')  # 회원가입 실패 메시지
        else:
            st.error('비밀번호가 일치하지 않습니다.')
    else:
        st.warning("아이디, 비밀번호, 비밀번호 확인을 모두 입력해 주세요.")
