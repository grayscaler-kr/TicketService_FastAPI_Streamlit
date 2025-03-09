import streamlit as st
import requests
import re
from datetime import datetime

# FastAPI 서버 주소
API_URL = "http://localhost:8000/check_duplicate"
RESERVE_API_URL = "http://localhost:8000/reserve"

st.title("티켓 예약 시스템")

# 신청자 정보 입력
st.subheader("신청자 정보 입력")
name = st.text_input("이름 (5글자 이내, 한국어만)")
phone = st.text_input("전화번호 (11자, 숫자만)")
birth_date = st.date_input("생년월일", min_value=datetime(1900, 1, 1))

# 입력 검증 함수
def validate_inputs():
    if not re.match(r'^[가-힣]{1,5}$', name):
        st.error("이름은 한글 1~5자만 가능합니다.")
        return False
    if not re.match(r'^\d{11}$', phone):
        st.error("전화번호는 숫자 11자만 입력해주세요.")
        return False
    return True

# 중복 신청 확인
if st.button("중복 확인"):
    if validate_inputs():
        response = requests.post(API_URL, json={"name": name, "phone": phone, "birth_date": str(birth_date)})
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
ticket_options = {"VIP석": "vip.jpg", "R석": "r_seat.jpg", "S석": "s_seat.jpg", "A석": "a_seat.jpg"}
ticket_choice = st.selectbox("티켓 선택", list(ticket_options.keys()))
# st.image(ticket_options[ticket_choice], caption=ticket_choice, use_container_width=True)

# 좌석 배열 정의 (간단한 5x5 예제)
rows = ["VIP", "R", "S", "A",]

# 세션 상태에 선택된 좌석 저장
if "selected_areas" not in st.session_state:
    st.session_state.selected_areas = 'no'

st.subheader("공연장 좌석 선택 시스템")
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

# # 인원 선택 (좌석이 선택되지 않으면 비활성화)
# num_people = st.number_input(
#     "인원 선택",
#     min_value=1,
#     max_value=10,
#     step=1,
#     disabled=not seat_selected  # 좌석이 선택되지 않으면 비활성화
# )

# # 가격 계산
# selected_seat = st.session_state.selected_areas.split('_')[0] if '_' in st.session_state.selected_areas else st.session_state.selected_areas
# ticket_prices = {"VIP석": 300000, "R석": 200000, "S석": 150000, "A석": 100000}
# total_price = ticket_prices[selected_seat] * num_people if seat_selected else 0
# st.write(f"총 가격: {total_price:,}원")

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
        response = requests.post(RESERVE_API_URL, json=reservation_data)
        if response.status_code == 200:
            st.success("예약이 신청되었습니다!")
        else:
            st.error("예약 신청 실패. 다시 시도해주세요.")