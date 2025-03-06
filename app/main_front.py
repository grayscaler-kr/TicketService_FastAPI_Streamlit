import streamlit as st

FASTAPI_URL = "http://localhost:8000"
LOGIN_PAGE_URL = "http://localhost:8501"

# 페이지 제목
st.title("HAO's TicketBox")

# 상단 레이아웃 (상좌 - 티켓 리스트, 상우 - 로그인 버튼)
col1, col2 = st.columns([5, 1])  # 두 개의 컬럼을 설정 (비율로 크기 조정)
with col1:
    st.subheader("티켓 리스트 페이지입니다.")  # 티켓 리스트 페이지 문구
with col2:
    login_button = st.button("로그인")  # 로그인 버튼
    if login_button:
        st.markdown(f'<meta http-equiv="refresh" content="0; url={LOGIN_PAGE_URL}">', unsafe_allow_html=True)

# 중간 레이아웃 (티켓 리스트 영역)
st.markdown("---")  # 구분선

# 티켓 리스트 (중앙에 표시될 부분)
st.header("티켓 리스트")

# 티켓 리스트를 여러 개의 카드 형태로 표시 (각각 썸네일과 간략 설명)
ticket_data = [
    {"thumbnail": "https://via.placeholder.com/150", "description": "티켓 1: 이곳에서 특별한 공연을 만나보세요!", "ticket_id": 1},
    {"thumbnail": "https://via.placeholder.com/150", "description": "티켓 2: 최고의 콘서트를 놓치지 마세요!", "ticket_id": 2},
    {"thumbnail": "https://via.placeholder.com/150", "description": "티켓 3: 전시회를 즐기세요!", "ticket_id": 3},
]

# 티켓 리스트 출력
for ticket in ticket_data:
    col1, col2 = st.columns([1, 3])  # 썸네일과 설명을 나누는 두 개의 컬럼
    with col1:
        # 이미지를 클릭하면 예매 페이지로 이동
        st.markdown(f'<a href="/booking/{ticket["ticket_id"]}" target="_self"><img src="{ticket["thumbnail"]}" width="100" /></a>', unsafe_allow_html=True)  
    with col2:
        st.write(ticket["description"])  # 간략 설명

