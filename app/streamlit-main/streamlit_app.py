import io
import os
import numpy as np
import requests
import streamlit as st
from PIL import Image
from streamlit_image_select import image_select


# 절대 경로로 로컬 이미지를 로드
abs_img_path = '/web/images'
top_img_path = f'{abs_img_path}/hao2.jpg'

# 페이지 설정 (타이틀 텍스트 설정)
st.set_page_config(page_title="HAO TICKET", page_icon="🎟️")

# 여백을 주기 위한 마크다운 수정
st.markdown('<style>div.block-container {padding-top: 3rem; padding-bottom: 1rem;}</style>', unsafe_allow_html=True)

# 두 개의 열로 나누기: 첫 번째 열은 이미지, 두 번째 열은 타이틀 텍스트
col1, col2 = st.columns([1, 4])  # 첫 번째 열은 좁고, 두 번째 열은 넓게

# 티켓 이미지 표시 (첫 번째 열에)
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

# "Select the Ticket" 부분 꾸미기
st.markdown(
    f'<div style="background-color: #000000; padding: 10px 20px; border-radius: 10px; text-align: center; color: white; font-size: 30px; font-weight: bold; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); margin-left: auto; margin-right: auto; width: fit-content; margin-top: 20px;">'
    f'Select the Ticket'
    f'</div>',
    unsafe_allow_html=True,
)



# 이미지 크기 지정
image_width = 300  # 원하는 가로 크기
image_height = 300  # 원하는 세로 크기

# 이미지 선택 (4개의 이미지를 한 번에 표시)
img = image_select(
    label="",
    images=[
        Image.open(f"{abs_img_path}/2ne1.jpg"),
        Image.open(f"{abs_img_path}/jj.jpg"),
        Image.open(f"{abs_img_path}/hero.jpg"),
        Image.open(f"{abs_img_path}/iu.jpg"),
    ],
    captions=["2NE1", "Kim Jae Joong", "IM HERO", "IU"]
)

# 선택된 이미지에 따른 추가 동작
if isinstance(img, np.ndarray) or isinstance(img, Image.Image):
    # 이미지 표시 (이미지 클릭 시 해당 열에서 중앙 정렬)
    st.image(img, width=image_width, use_container_width=True)
