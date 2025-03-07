import sys, os

# app/fastapi-app/ 상대 경로로 routers 디렉토리가 포함된 디렉토리 경로 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import streamlit as st
import requests
# import log
import configparser

config = configparser.ConfigParser()
config.read('/test-FastAPI/app/config.ini')

# URL 가져오기
# Fastapi login url
LOGIN_URL = config['FASTAPI_URL']['LOGIN_URL']

# streamlit main url - front connect
MAIN_URL = config['STREAMLIT_URL']['MAIN_URL']
USER_URL = config['STREAMLIT_URL']['USER_URL']


# 로그인 폼
st.title("로그인 페이지")

username = st.text_input("아이디")
password = st.text_input("비밀번호", type="password")

# 버튼 레이아웃 설정 (로그인 버튼과 회원가입 버튼을 옆에 배치)
col1, col2 = st.columns([3, 1])  # 첫 번째 버튼은 더 넓게, 두 번째 버튼은 좁게 설정

with col1:
    if st.button("Login"):
        # 로그인 정보가 입력되었는지 확인
        if username and password:
            # FastAPI의 로그인 엔드포인트로 POST 요청
            url = LOGIN_URL  # FastAPI 서버 URL (로그인 엔드포인트)
            data = {
                "username": username,
                "password": password
            }

            # POST 요청을 보내고 응답 받기
            response = requests.post(url, json=data)

            if response.status_code == 200:
                jwt_token = response.json().get("access_token")
                st.success('로그인 성공')  # 로그인 성공
                st.markdown(f'<meta http-equiv="refresh" content="0; url={MAIN_URL}?access_token={jwt_token}">', unsafe_allow_html=True)
            else:
                st.error('로그인 실패')  # 로그인 실패
        else:
            st.warning("아이디와 비밀번호를 입력해 주세요.")  # 입력 값이 없으면 경고 메시지

with col2:
    if st.button("회원가입"):
        # 회원가입 버튼 클릭 시 처리
        # 예시로 회원가입 페이지 URL을 메인 페이지로 설정해도 됩니다.
        st.markdown(f'<meta http-equiv="refresh" content="0; url={USER_URL}">', unsafe_allow_html=True)
