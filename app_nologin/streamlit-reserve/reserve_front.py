import streamlit as st
import requests
import configparser

config = configparser.ConfigParser()
config.read('/test-FastAPI/app/config.ini')

# URL 가져오기
MAIN_URL = config['FASTAPI_URL']['MAIN_URL']
LOGIN_URL = config['FASTAPI_URL']['LOGIN_URL']
RESERVE_URL = config['FASTAPI_URL']['RESERVE_URL']
USER_URL = config['FASTAPI_URL']['USER_URL']

st.title("예약 페이지")

# 사용자 입력
user_id = st.number_input("사용자 ID", min_value=1)
item_id = st.number_input("아이템 ID", min_value=1)
date = st.date_input("예약 날짜")

if st.button("예약하기"):
    # 예약 요청
    response = requests.post(
        "http://fastapi-app:8000/reserve",
        json={"user_id": user_id, "item_id": item_id, "date": str(date)}
    )
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error("예약 실패")
