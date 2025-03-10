import streamlit as st
import configparser
from PIL import Image
from streamlit_image_select import image_select
import numpy as np
import os

config = configparser.ConfigParser()
config.read('/test-FastAPI/app_nologin/config.ini')

# region URL 가져오기
MAIN_URL = config['STREAMLIT_URL']['MAIN_URL']
RESERVE_URL = config['STREAMLIT_URL']['RESERVE_URL']
#endregion

# region image path 정보
abs_img_path = '/test-FastAPI/app_nologin/streamlit-main/images'
top_img_path = f'{abs_img_path}/hao2.jpg'
first_img_path = f"{abs_img_path}/2ne1.jpg"
second_img_path = f"{abs_img_path}/jj.jpg"
thrid_img_path = f"{abs_img_path}/hero.jpg"
fourth_img_path = f"{abs_img_path}/iu.jpg"
# endregion

# region 이미지 크기 지정
image_width = 450  # 원하는 가로 크기
image_height = 600  # 원하는 세로 크기
# endregion

### token 값 확인
query_params = st.query_params
jwt_token = query_params.get("access_token", [None])[0]

# region 타이틀 설정 (타이틀 텍스트 설정)
st.set_page_config(page_title="HAO TICKET", page_icon="🎟️")
# 여백을 주기 위한 마크다운 수정
st.markdown('<style>div.block-container {padding-top: 3rem; padding-bottom: 1rem;}</style>', unsafe_allow_html=True)

# 두 개의 열로 나누기: 첫 번째 열은 이미지, 두 번째 열은 타이틀 텍스트
col1, col2 = st.columns([1, 4])  # 첫 번째 열은 좁고, 두 번째 열은 넓게

# 이미지 표시 (첫 번째 열에)
with col1:
    img = Image.open(top_img_path)
    st.image(img, width=100)  # 이미지 크기를 100px로 설정

# 타이틀 텍스트 표시 (두 번째 열에, 이미지 중간에 맞추기)
with col2:
    st.markdown(
        f'<div style="display: flex; align-items: center; height: 100px; margin-left: -40px;">'  # 글씨를 더 왼쪽으로 이동
        f'<span style="font-size: 60px; white-space: nowrap; margin-top: 20px;">Welcome to HAO TICKET!</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
# endregion

# region
_, col3, _ = st.columns([2, 2, 1])
with col3:
    reserve_button = st.button("예약하러가기")  # 예약 버튼

    st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #000000;
        font-size: 30px;
        padding: 10px 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-weight: bold;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        width: fit-content;
        margin-top: 20px;
        height: 50px; /* 높이 통일 */
        display: flex;
        align-items: center; /* 세로 중앙 정렬 */
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

    if reserve_button:
        # 예약 페이지로 리디렉션
        st.markdown(f'<meta http-equiv="refresh" content="0; url={RESERVE_URL}">', unsafe_allow_html=True)
    
    
# endregion


# region 이미지 선택 (4개의 이미지를 한 번에 표시)
img = image_select(
    label="",
    images=[
        Image.open(first_img_path),
        Image.open(second_img_path),
        Image.open(thrid_img_path),
        Image.open(fourth_img_path),
    ],
    captions=["2NE1", "Kim Jae Joong", "IM HERO", "IU"]
)

filename = os.path.basename(img.filename).split(".")[0]
resized_img = img.resize((image_width, image_height))
# print(filename)

# 선택된 이미지에 따른 추가 동작
if isinstance(img, np.ndarray) or isinstance(img, Image.Image):
    # 이미지 표시 (이미지 클릭 시 해당 열에서 중앙 정렬)
    # st.image(img, width=image_width, use_container_width=True)
    col5, col6 = st.columns([1, 1]) 
    with col5:
        st.image(resized_img)
    with col6:
        st.write(f"{filename} 티켓 정보: ~~~~~~~")
# endregion