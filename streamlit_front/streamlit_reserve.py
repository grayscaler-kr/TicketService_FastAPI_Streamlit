import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import streamlit as st
import requests
import os
from datetime import datetime
import configparser
from common.validation import validate_name, validate_phone_number

config = configparser.ConfigParser()
config.read('/test-FastAPI/streamlit_front/common/config.ini')

# URL 가져오기
RESERVE_URL = config['FASTAPI_URL']['RESERVE_URL']
VERIFY_URL = config['FASTAPI_URL']['VERIFY_URL']
CHECK_DUPLICATE_URL = config['FASTAPI_URL']['CHECK_DUPLICATE_URL']

#region 파일 리스트 및 이름
image_list = os.listdir("/test-FastAPI/streamlit_front/images/ticket")
ticket_list = sorted([i.split(".")[0] for i in image_list])
#endregion

# region session 값 확인
if st.session_state.logged_in == False:
    st.switch_page("streamlit_login.py")

if "selected_image" not in st.session_state:
    st.session_state.selected_image = ticket_list[0]
# endregion



# page start
st.title("티켓 예약 시스템")

# 신청자 정보 입력
st.subheader("신청자 정보 입력")
use_existing_info = st.checkbox("가입자 정보와 일치")
# 사용자 정보를 가져와서 기본 값으로 채워넣기
if use_existing_info:
    # 현재 로그인된 사용자 토큰 가져오기
    jwt_token = st.session_state.get("jwt_token")
    if jwt_token:
        print(jwt_token)
        response = requests.post(VERIFY_URL, headers={"Authorization": f"Bearer {jwt_token}"})
        if response.status_code == 200:
            result = response.json()
            if result["user_info_matched"]:
                # 일치하는 사용자 정보가 있을 때
                name = result["name"]
                phone = result["phone"]
                birth_date = result["birth_date"]
                # 사용자가 정보를 수정할 수 없도록 비활성화
                st.text_input("이름", value=name, disabled=True)
                st.text_input("전화번호", value=phone, disabled=True)
                st.date_input("생년월일", value=datetime.strptime(birth_date, "%Y-%m-%d"), disabled=True)
            else:
                st.error("일치 x")
        else:
            st.error("정보를 불러오는 데 실패했습니다.")
else:
    # 직접 입력 받기
    name = st.text_input("이름 (5글자 이내, 한국어만)")
    phone = st.text_input("전화번호 (11자, 숫자만)")
    birth_date = st.date_input("생년월일", min_value=datetime(1900, 1, 1))


# 중복 신청 확인
if st.button("중복 확인"):
    valid_result = validate_name(name)
    if valid_result:
        st.warning(valid_result[1])
    else:
        valid_result = validate_phone_number(phone)
        if valid_result:
            st.warning(valid_result[1])
        else:
            response = requests.post(CHECK_DUPLICATE_URL, json={"name": name, "phone_number": phone, "dob": str(birth_date)})
            if response.status_code == 200:
                result = response.json()
                if result["duplicate"]:
                    st.error("이미 신청된 정보입니다!")
                else:
                    st.success("신청 가능합니다.")
            else:
                st.error("서버 오류 발생. 다시 시도해주세요.")

# 티켓 선택
st.subheader("티켓 선택")
ticket_choice = st.selectbox("티켓 선택", ticket_list, index=ticket_list.index(st.session_state.selected_image))
# st.image(ticket_options[ticket_choice], caption=ticket_choice, use_container_width=True)

# 좌석 배열 정의 (간단한 5x5 예제)
rows = ["VIP", "R", "S", "A",]

# 세션 상태에 선택된 좌석 저장
if "selected_areas" not in st.session_state:
    st.session_state.selected_areas = 'no'

st.markdown("공연장 좌석 선택 시스템")
st.markdown(
    f'<div style="background-color: #000000; padding: 10px 10px; border-radius: 10px; text-align: center; color: white; font-size: 30px; font-weight: bold; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); margin-left: auto; margin-right: auto; width: margin-top: 20px;">'
    f'STAGE'
    f'</div>',
    unsafe_allow_html=True,
)

# 버튼 스타일 지정 함수
def area_button(area_name, key_name, col):
    if col.button(area_name, key=key_name, use_container_width=True):
        st.session_state.selected_areas = key_name

# 첫 번째 줄 (R석 - VIP석 - R석)
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    area_button("R석", "R석_1", col1)
with col2:
    area_button("VIP석", "VIP석", col2)
with col3:
    area_button("R석", "R석_2", col3)

# 두 번째 줄 (S석 - R석 - S석)
col4, col5, col6 = st.columns([1, 3, 1])
with col4:
    area_button("S석", "S석_1", col4)
with col5:
    area_button("R석", "R석_3", col5)
with col6:
    area_button("S석", "S석_2", col6)

# 마지막 줄 (A석 - A석)
col7, _, _, col8 = st.columns([1, 2, 2, 1])
with col7:
    area_button("A석", "A석_1", col7)
with col8:
    area_button("A석", "A석_2", col8)


# 선택된 영역 표시
st.subheader("선택된 좌석")

if st.session_state.selected_areas == 'no':
    st.write("선택된 좌석이 없습니다.")
else: st.write(st.session_state.selected_areas)



# 좌석이 선택되지 않은 경우 버튼 비활성화
seat_selected = st.session_state.selected_areas != "no"

# 선택된 좌석 확인
selected_seat = st.session_state.selected_areas.split('_')[0] if '_' in st.session_state.selected_areas else st.session_state.selected_areas
ticket_prices = {"VIP석": 300000, "R석": 200000, "S석": 150000, "A석": 100000}


# 인원 선택 부분
num_people = st.number_input(
    "인원 선택",
    min_value=1,
    max_value=10,
    step=1,
    disabled=not seat_selected,  # 좌석이 선택되지 않으면 비활성화
    label_visibility="collapsed"  # 라벨 숨기기
)

# 가격 계산
total_price = ticket_prices[selected_seat] * num_people if seat_selected else 0

# 가격을 `st.metric`으로 강조
if seat_selected:
    st.metric("총 가격", f"{total_price:,}원", delta=None)


# 예약 신청 버튼
if st.button("예약 신청", disabled=not seat_selected):  # 좌석이 선택되지 않으면 비활성화
    if validate_inputs():
        reservation_data = {
            "name": name,
            "phone": phone,
            "birth_date": str(birth_date),
            "ticket": ticket_choice,
            "num_people": num_people,
            "total_price": total_price
        }
        response = requests.post(RESERVE_URL, json=reservation_data)
        if response.status_code == 200:
            st.success("예약이 신청되었습니다!")
        else:
            st.error("예약 신청 실패. 다시 시도해주세요.")